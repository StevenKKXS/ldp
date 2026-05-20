if __name__ == "__main__":
    import os
    import pathlib
    import sys

    ROOT_DIR = str(pathlib.Path(__file__).parent.parent.parent)
    sys.path.append(ROOT_DIR)
    os.chdir(ROOT_DIR)

import copy
import csv
import json
import os
import pathlib
import random
import time

import hydra
import numpy as np
import torch
import torch.nn.functional as F
import tqdm
from omegaconf import OmegaConf
from torch.utils.data import DataLoader

from diffusion_policy.common.json_logger import JsonLogger
from diffusion_policy.common.pytorch_util import dict_apply, optimizer_to
from diffusion_policy.dataset.base_dataset import BaseImageDataset
from diffusion_policy.workspace.base_workspace import BaseWorkspace

OmegaConf.register_new_resolver("eval", eval, replace=True)


class TrainBehaviorTranslatorWorkspace(BaseWorkspace):
    include_keys = ["global_step", "epoch", "best_metric"]

    def __init__(self, cfg: OmegaConf, output_dir=None):
        super().__init__(cfg, output_dir=output_dir)

        seed = cfg.training.seed
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)

        obs_policy = hydra.utils.instantiate(cfg.obs_encoder_policy)
        self.obs_encoder = obs_policy.obs_encoder
        obs_dim = int(obs_policy.obs_feature_dim)
        del obs_policy

        self.model = hydra.utils.instantiate(cfg.model, obs_dim=obs_dim)
        self.optimizer = torch.optim.AdamW(
            [
                {
                    "params": self.obs_encoder.parameters(),
                    "lr": cfg.optimizer.obs_encoder_lr,
                    "weight_decay": cfg.optimizer.obs_encoder_weight_decay,
                },
                {
                    "params": self.model.parameters(),
                    "lr": cfg.optimizer.translator_lr,
                    "weight_decay": cfg.optimizer.translator_weight_decay,
                },
            ],
            betas=tuple(cfg.optimizer.betas),
        )

        self.global_step = 0
        self.epoch = 0
        self.best_metric = None

    def _move_obs_to_device(self, obs, device):
        return dict_apply(obs, lambda x: x.to(device, non_blocking=True))

    def _encode_obs(self, obs, normalizer, device):
        obs = self._move_obs_to_device(obs, device)
        nobs = normalizer.normalize(obs)
        if "embedding" in obs:
            nobs["embedding"] = obs["embedding"]

        value = next(iter(nobs.values()))
        bsz, horizon = value.shape[:2]
        flat_obs = dict_apply(nobs, lambda x: x.reshape(bsz * horizon, *x.shape[2:]))
        obs_tokens = self.obs_encoder(flat_obs).reshape(bsz, horizon, -1)
        return obs_tokens

    def _compute_batch(self, batch, normalizer, device):
        obs_tokens = self._encode_obs(batch["obs"], normalizer, device)
        act_past = batch["act_past"].to(device, non_blocking=True)
        act_future = batch["act_future"].to(device, non_blocking=True)
        act_past = normalizer["action"].normalize(act_past)
        act_future = normalizer["action"].normalize(act_future)

        result = self.model(obs_tokens, return_context=True)
        pred = result["pred_actions"]
        model = self.model.module if isinstance(self.model, torch.nn.DataParallel) else self.model
        p = model.past_action_horizon
        pred_past = pred[:, :p]
        pred_future = pred[:, p:]

        loss_past = F.smooth_l1_loss(pred_past, act_past) if p > 0 else pred.sum() * 0
        loss_future = F.smooth_l1_loss(pred_future, act_future)
        target_mode = self.cfg.training.target_mode
        if target_mode == "past":
            loss_total = loss_past
        elif target_mode == "future":
            loss_total = loss_future
        elif target_mode == "past_future":
            loss_total = (
                float(self.cfg.training.w_past) * loss_past
                + float(self.cfg.training.w_future) * loss_future
            )
        else:
            raise ValueError(f"Unsupported target_mode: {target_mode}")

        with torch.no_grad():
            future_l1_by_h = torch.mean(torch.abs(pred_future - act_future), dim=(0, 2))
            gripper_acc = torch.mean(
                (torch.sign(pred_future[..., -1]) == torch.sign(act_future[..., -1])).float()
            )
            metrics = {
                "loss_total": loss_total.detach(),
                "loss_past": loss_past.detach(),
                "loss_future": loss_future.detach(),
                "past_l1": torch.mean(torch.abs(pred_past - act_past)).detach() if p > 0 else loss_total.detach() * 0,
                "future_l1": torch.mean(torch.abs(pred_future - act_future)).detach(),
                "future_mse": F.mse_loss(pred_future, act_future).detach(),
                "gripper_acc": gripper_acc.detach(),
            }
            for i, value in enumerate(future_l1_by_h):
                metrics[f"per_horizon_future_l1_{i:02d}"] = value.detach()

        return loss_total, metrics

    def _mean_metrics(self, metrics_list):
        result = dict()
        if len(metrics_list) == 0:
            return result
        keys = metrics_list[0].keys()
        for key in keys:
            result[key] = float(torch.stack([x[key].detach().cpu() for x in metrics_list]).mean())
        return result

    def _write_metrics_csv(self, path, row):
        path = pathlib.Path(path)
        is_new = not path.exists()
        with path.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row.keys()))
            if is_new:
                writer.writeheader()
            writer.writerow(row)

    def _save_checkpoint_epoch(self, epoch_idx, val_metric):
        is_best = self.best_metric is None or val_metric < self.best_metric
        if is_best:
            self.best_metric = float(val_metric)

        self.save_checkpoint(tag="latest", use_thread=False)
        if (epoch_idx % int(self.cfg.training.checkpoint_every)) == 0:
            self.save_checkpoint(tag=f"epoch_{epoch_idx:04d}", use_thread=False)

        if is_best:
            self.save_checkpoint(tag="best", use_thread=False)

    def run(self):
        cfg = copy.deepcopy(self.cfg)
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        OmegaConf.save(config=cfg, f=os.path.join(self.output_dir, "config.yaml"))

        if cfg.training.resume and self.get_checkpoint_path().is_file():
            self.load_checkpoint(path=self.get_checkpoint_path())

        dataset: BaseImageDataset = hydra.utils.instantiate(cfg.task.dataset)
        assert isinstance(dataset, BaseImageDataset)
        train_dataloader = DataLoader(dataset, **cfg.dataloader)
        val_dataset = dataset.get_validation_dataset()
        val_dataloader = DataLoader(val_dataset, **cfg.val_dataloader)
        normalizer = dataset.get_normalizer()

        device = torch.device(cfg.training.device)
        self.obs_encoder.to(device)
        self.model.to(device)
        normalizer.to(device)
        optimizer_to(self.optimizer, device)
        if bool(cfg.training.get("data_parallel", False)):
            n_devices = torch.cuda.device_count() if device.type == "cuda" else 0
            if n_devices > 1:
                self.obs_encoder = torch.nn.DataParallel(self.obs_encoder)
                self.model = torch.nn.DataParallel(self.model)
                print(f"Enabled DataParallel over {n_devices} CUDA devices.")

        env_info = {
            "python": os.sys.executable,
            "torch": torch.__version__,
        }
        try:
            import robomimic
            env_info["robomimic_version"] = getattr(robomimic, "__version__", None)
            env_info["robomimic_file"] = getattr(robomimic, "__file__", None)
        except Exception as exc:
            env_info["robomimic_error"] = repr(exc)
        with open(os.path.join(self.output_dir, "env.json"), "w") as f:
            json.dump(env_info, f, indent=2)

        log_path = os.path.join(self.output_dir, "logs.json.txt")
        metrics_csv = os.path.join(self.output_dir, "metrics.csv")
        with JsonLogger(log_path) as json_logger:
            for local_epoch_idx in range(int(cfg.training.num_epochs)):
                epoch_idx = self.epoch + 1
                self.obs_encoder.train()
                self.model.train()
                train_metrics = []
                train_data_times = []
                train_compute_times = []
                optimizer_zeroed = False
                self.optimizer.zero_grad(set_to_none=True)

                train_iter = tqdm.tqdm(
                    train_dataloader,
                    desc=f"Training epoch {epoch_idx}",
                    leave=False,
                    mininterval=float(cfg.training.tqdm_interval_sec))
                last_iter_end = time.perf_counter()
                for batch_idx, batch in enumerate(train_iter):
                    iter_start = time.perf_counter()
                    train_data_times.append(iter_start - last_iter_end)
                    if bool(cfg.training.get("profile_sync_cuda", False)) and device.type == "cuda":
                        torch.cuda.synchronize(device)
                    compute_start = time.perf_counter()
                    loss, metrics = self._compute_batch(batch, normalizer, device)
                    loss = loss / int(cfg.training.gradient_accumulate_every)
                    loss.backward()
                    optimizer_zeroed = False

                    if ((batch_idx + 1) % int(cfg.training.gradient_accumulate_every)) == 0:
                        if cfg.training.grad_clip is not None:
                            torch.nn.utils.clip_grad_norm_(
                                list(self.obs_encoder.parameters()) + list(self.model.parameters()),
                                float(cfg.training.grad_clip))
                        self.optimizer.step()
                        self.optimizer.zero_grad(set_to_none=True)
                        optimizer_zeroed = True
                        self.global_step += 1

                    train_metrics.append(metrics)
                    if bool(cfg.training.get("profile_sync_cuda", False)) and device.type == "cuda":
                        torch.cuda.synchronize(device)
                    iter_end = time.perf_counter()
                    train_compute_times.append(iter_end - compute_start)
                    last_iter_end = iter_end
                    if cfg.training.max_train_steps is not None and batch_idx >= int(cfg.training.max_train_steps) - 1:
                        break

                if not optimizer_zeroed:
                    if cfg.training.grad_clip is not None:
                        torch.nn.utils.clip_grad_norm_(
                            list(self.obs_encoder.parameters()) + list(self.model.parameters()),
                            float(cfg.training.grad_clip))
                    self.optimizer.step()
                    self.optimizer.zero_grad(set_to_none=True)
                    self.global_step += 1

                self.obs_encoder.eval()
                self.model.eval()
                val_metrics = []
                with torch.no_grad():
                    for batch_idx, batch in enumerate(val_dataloader):
                        _, metrics = self._compute_batch(batch, normalizer, device)
                        val_metrics.append(metrics)
                        if cfg.training.max_val_batches is not None and batch_idx >= int(cfg.training.max_val_batches) - 1:
                            break

                train_log = self._mean_metrics(train_metrics)
                if train_data_times:
                    train_log["data_time_mean"] = float(np.mean(train_data_times))
                    train_log["data_time_max"] = float(np.max(train_data_times))
                    train_log["data_time_total"] = float(np.sum(train_data_times))
                if train_compute_times:
                    train_log["compute_time_mean"] = float(np.mean(train_compute_times))
                    train_log["compute_time_max"] = float(np.max(train_compute_times))
                    train_log["compute_time_total"] = float(np.sum(train_compute_times))
                val_log = self._mean_metrics(val_metrics)
                step_log = {
                    "epoch": epoch_idx,
                    "global_step": self.global_step,
                }
                step_log.update({f"train/{k}": v for k, v in train_log.items()})
                step_log.update({f"val/{k}": v for k, v in val_log.items()})

                monitor_key = cfg.training.monitor_key
                monitor_value = step_log[monitor_key]
                self.epoch = epoch_idx
                self._save_checkpoint_epoch(epoch_idx, monitor_value)
                step_log["best_metric"] = float(self.best_metric)
                json_logger.log(step_log)
                self._write_metrics_csv(metrics_csv, step_log)


@hydra.main(
    version_base=None,
    config_path=str(pathlib.Path(__file__).parent.parent.joinpath("config")),
    config_name=pathlib.Path(__file__).stem)
def main(cfg):
    workspace = TrainBehaviorTranslatorWorkspace(cfg)
    workspace.run()


if __name__ == "__main__":
    main()
