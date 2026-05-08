"""Task-local scheduled DP workspaces for Square no-history experiments.

These classes intentionally live under the task directory so the shared LDP
source tree can be used read-only on the GPU machine. They mirror the native
UNet and transformer image workspaces, adding only epoch scheduling and named
checkpoint retention.
"""

from __future__ import annotations

import copy
import os
import random

import hydra
import numpy as np
import torch
import tqdm
import wandb
from omegaconf import OmegaConf
from torch.utils.data import DataLoader

from diffusion_policy.common.checkpoint_util import TopKCheckpointManager
from diffusion_policy.common.json_logger import JsonLogger
from diffusion_policy.common.pytorch_util import dict_apply, optimizer_to
from diffusion_policy.dataset.base_dataset import BaseImageDataset
from diffusion_policy.env_runner.base_image_runner import BaseImageRunner
from diffusion_policy.model.common.lr_scheduler import get_scheduler
from diffusion_policy.model.diffusion.ema_model import EMAModel
from diffusion_policy.policy.diffusion_transformer_hybrid_image_policy import (
    DiffusionTransformerHybridImagePolicy,
)
from diffusion_policy.policy.diffusion_unet_image_policy import DiffusionUnetImagePolicy
from diffusion_policy.workspace.base_workspace import BaseWorkspace
from hsic import batch_hsic


OmegaConf.register_new_resolver("eval", eval, replace=True)


def _select(cfg, key, default=None):
    value = OmegaConf.select(cfg, key)
    return default if value is None else value


class _ScheduledImageWorkspaceMixin:
    include_keys = ["global_step", "epoch"]

    def _is_scheduled_epoch(self, cfg: OmegaConf, name: str) -> bool:
        human_epoch = self.epoch + 1
        explicit_epochs = _select(cfg.training, f"{name}_epochs")
        if explicit_epochs is not None:
            return human_epoch in {int(x) for x in explicit_epochs}

        if bool(_select(cfg.training, f"{name}_final", True)):
            if human_epoch == int(cfg.training.num_epochs):
                return True

        early_until = int(_select(cfg.training, "schedule_early_until", 100))
        early_every = int(
            _select(
                cfg.training,
                f"{name}_early_every",
                _select(cfg.training, "schedule_early_every", 10),
            )
        )
        late_every = int(
            _select(
                cfg.training,
                f"{name}_late_every",
                _select(cfg.training, "schedule_late_every", 100),
            )
        )
        if human_epoch <= early_until:
            return early_every > 0 and (human_epoch % early_every) == 0
        return late_every > 0 and (human_epoch % late_every) == 0

    def _is_interval_epoch(self, cfg: OmegaConf, key: str) -> bool:
        interval = int(_select(cfg.training, key, 0))
        return interval > 0 and ((self.epoch + 1) % interval) == 0

    def _apply_debug_overrides(self, cfg: OmegaConf) -> None:
        if not cfg.training.debug:
            return
        if "env_runner" in cfg.task:
            cfg.task.env_runner.n_envs = min(int(cfg.task.env_runner.n_envs), 4)
            cfg.task.env_runner.n_test = min(int(cfg.task.env_runner.n_test), 2)
            cfg.task.env_runner.n_test_vis = min(int(cfg.task.env_runner.n_test_vis), 2)
            cfg.task.env_runner.n_train = min(int(cfg.task.env_runner.n_train), 2)
            cfg.task.env_runner.n_train_vis = min(int(cfg.task.env_runner.n_train_vis), 2)
        cfg.training.num_epochs = 2
        cfg.training.max_train_steps = 2
        cfg.training.max_val_steps = 2
        cfg.training.schedule_early_every = 1
        cfg.training.schedule_late_every = 1
        cfg.training.val_every = 1
        cfg.training.sample_every = 1

    def _save_scheduled_checkpoints(
        self,
        cfg: OmegaConf,
        step_log: dict,
        topk_manager: TopKCheckpointManager,
    ) -> None:
        ckpt_dir = os.path.join(self.output_dir, "checkpoints")
        os.makedirs(ckpt_dir, exist_ok=True)

        if cfg.checkpoint.save_last_ckpt:
            self.save_checkpoint(use_thread=False)
        if cfg.checkpoint.save_last_snapshot:
            self.save_snapshot()

        human_epoch = self.epoch + 1
        if bool(_select(cfg.checkpoint, "save_epoch_ckpt", True)):
            epoch_ckpt_path = os.path.join(ckpt_dir, f"epoch={human_epoch:04d}.ckpt")
            self.save_checkpoint(path=epoch_ckpt_path, use_thread=False)
            step_log["epoch_ckpt_path"] = epoch_ckpt_path

        metric_dict = {}
        for key, value in step_log.items():
            if isinstance(value, (int, float, np.floating, np.integer)):
                metric_dict[key.replace("/", "_")] = value
        metric_dict["epoch"] = human_epoch
        metric_dict["global_step"] = self.global_step

        monitor_key = cfg.checkpoint.topk.monitor_key
        if monitor_key in metric_dict:
            topk_ckpt_path = topk_manager.get_ckpt_path(metric_dict)
            if topk_ckpt_path is not None:
                self.save_checkpoint(path=topk_ckpt_path, use_thread=False)

    def _run_scheduled(self, probe_dataset: bool = False) -> None:
        cfg = copy.deepcopy(self.cfg)

        if cfg.training.resume:
            latest_ckpt_path = self.get_checkpoint_path()
            if latest_ckpt_path.is_file():
                print(f"Resuming from checkpoint {latest_ckpt_path}")
                self.load_checkpoint(path=latest_ckpt_path)

        dataset = hydra.utils.instantiate(cfg.task.dataset)
        assert isinstance(dataset, BaseImageDataset)
        if probe_dataset:
            dataset.__getitem__(0)
        train_dataloader = DataLoader(dataset, **cfg.dataloader)
        normalizer = dataset.get_normalizer()

        val_dataset = dataset.get_validation_dataset()
        val_dataloader = DataLoader(val_dataset, **cfg.val_dataloader)

        self.model.set_normalizer(normalizer)
        if self.ema_model is not None:
            self.ema_model.set_normalizer(normalizer)

        lr_scheduler = get_scheduler(
            cfg.training.lr_scheduler,
            optimizer=self.optimizer,
            num_warmup_steps=cfg.training.lr_warmup_steps,
            num_training_steps=(len(train_dataloader) * cfg.training.num_epochs)
            // cfg.training.gradient_accumulate_every,
            last_epoch=self.global_step - 1,
        )

        ema = None
        if self.ema_model is not None:
            ema = hydra.utils.instantiate(cfg.ema, model=self.ema_model)

        self._apply_debug_overrides(cfg)

        env_runner = None
        if "env_runner" in cfg.task:
            env_runner = hydra.utils.instantiate(cfg.task.env_runner, output_dir=self.output_dir)
            assert isinstance(env_runner, BaseImageRunner)

        wandb_run = wandb.init(
            dir=str(self.output_dir),
            config=OmegaConf.to_container(cfg, resolve=True),
            **cfg.logging,
        )
        wandb.config.update({"output_dir": self.output_dir})

        topk_manager = TopKCheckpointManager(
            save_dir=os.path.join(self.output_dir, "checkpoints"),
            **cfg.checkpoint.topk,
        )

        device = torch.device(cfg.training.device)
        self.model.to(device)
        if self.ema_model is not None:
            self.ema_model.to(device)
        optimizer_to(self.optimizer, device)

        train_sampling_batch = None
        debug_loss = True
        log_path = os.path.join(self.output_dir, "logs.json.txt")
        with JsonLogger(log_path) as json_logger:
            for _ in range(cfg.training.num_epochs):
                step_log = {}

                self._pre_train_epoch(cfg)
                train_losses = []
                with tqdm.tqdm(
                    train_dataloader,
                    desc=f"Training epoch {self.epoch + 1}",
                    leave=False,
                    mininterval=cfg.training.tqdm_interval_sec,
                ) as tepoch:
                    for batch_idx, batch in enumerate(tepoch):
                        batch = dict_apply(batch, lambda x: x.to(device, non_blocking=True))
                        if train_sampling_batch is None:
                            train_sampling_batch = batch

                        raw_loss, debug_loss = self._compute_training_loss(batch, debug_loss)
                        loss = raw_loss / cfg.training.gradient_accumulate_every
                        loss.backward()

                        if self.global_step % cfg.training.gradient_accumulate_every == 0:
                            self.optimizer.step()
                            self.optimizer.zero_grad()
                            lr_scheduler.step()

                        if ema is not None:
                            ema.step(self.model)

                        raw_loss_cpu = raw_loss.item()
                        tepoch.set_postfix(loss=raw_loss_cpu, refresh=False)
                        train_losses.append(raw_loss_cpu)
                        step_log = {
                            "train_loss": raw_loss_cpu,
                            "global_step": self.global_step,
                            "epoch": self.epoch + 1,
                            "lr": lr_scheduler.get_last_lr()[0],
                        }

                        is_last_batch = batch_idx == (len(train_dataloader) - 1)
                        if not is_last_batch:
                            wandb_run.log(step_log, step=self.global_step)
                            json_logger.log(step_log)
                            self.global_step += 1

                        max_train_steps = cfg.training.max_train_steps
                        if max_train_steps is not None and batch_idx >= (max_train_steps - 1):
                            break

                step_log["train_loss"] = float(np.mean(train_losses))

                policy = self.ema_model if self.ema_model is not None else self.model
                policy.eval()

                if self._is_scheduled_epoch(cfg, "rollout") and env_runner is not None:
                    runner_log = env_runner.run(policy)
                    step_log.update(runner_log)

                if self._is_interval_epoch(cfg, "val_every"):
                    with torch.no_grad():
                        val_losses = []
                        with tqdm.tqdm(
                            val_dataloader,
                            desc=f"Validation epoch {self.epoch + 1}",
                            leave=False,
                            mininterval=cfg.training.tqdm_interval_sec,
                        ) as tepoch:
                            for batch_idx, batch in enumerate(tepoch):
                                batch = dict_apply(batch, lambda x: x.to(device, non_blocking=True))
                                loss = self._compute_validation_loss(batch)
                                val_losses.append(loss.detach())
                                max_val_steps = cfg.training.max_val_steps
                                if max_val_steps is not None and batch_idx >= (max_val_steps - 1):
                                    break
                        if len(val_losses) > 0:
                            step_log["val_loss"] = torch.stack(val_losses).mean().item()

                if self._is_interval_epoch(cfg, "sample_every"):
                    with torch.no_grad():
                        step_log.update(
                            self._compute_sample_metrics(policy, train_sampling_batch, device)
                        )

                if self._is_scheduled_epoch(cfg, "checkpoint"):
                    self._save_scheduled_checkpoints(cfg, step_log, topk_manager)

                policy.train()
                wandb_run.log(step_log, step=self.global_step)
                json_logger.log(step_log)
                self.global_step += 1
                self.epoch += 1

        if self._saving_thread is not None:
            self._saving_thread.join()
        wandb_run.finish()


class ScheduledDiffusionUnetImageWorkspace(_ScheduledImageWorkspaceMixin, BaseWorkspace):
    include_keys = ["global_step", "epoch"]

    def __init__(self, cfg: OmegaConf, output_dir=None):
        super().__init__(cfg, output_dir=output_dir)
        seed = cfg.training.seed
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)

        self.model: DiffusionUnetImagePolicy = hydra.utils.instantiate(cfg.policy)
        self.ema_model: DiffusionUnetImagePolicy | None = None
        if cfg.training.use_ema:
            self.ema_model = copy.deepcopy(self.model)

        self.optimizer = hydra.utils.instantiate(cfg.optimizer, params=self.model.parameters())
        self.global_step = 0
        self.epoch = 0

    def run(self):
        self._run_scheduled(probe_dataset=False)

    def _pre_train_epoch(self, cfg: OmegaConf) -> None:
        if cfg.training.freeze_encoder:
            self.model.obs_encoder.eval()
            self.model.obs_encoder.requires_grad_(False)

    def _compute_training_loss(self, batch, debug_loss: bool):
        return self.model.compute_loss(batch), False

    def _compute_validation_loss(self, batch):
        return self.model.compute_loss(batch)

    def _compute_sample_metrics(self, policy, train_sampling_batch, device):
        batch = dict_apply(train_sampling_batch, lambda x: x.to(device, non_blocking=True))
        obs_dict = batch["obs"]
        gt_action = batch["action"]
        result = policy.predict_action(obs_dict)
        pred_action = result["action_pred"]
        mse = torch.nn.functional.mse_loss(pred_action, gt_action)
        return {"train_action_mse_error": mse.item()}


class ScheduledDiffusionTransformerHybridWorkspace(_ScheduledImageWorkspaceMixin, BaseWorkspace):
    include_keys = ["global_step", "epoch"]

    def __init__(self, cfg: OmegaConf, output_dir=None):
        super().__init__(cfg, output_dir=output_dir)
        seed = cfg.training.seed
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)

        self.model: DiffusionTransformerHybridImagePolicy = hydra.utils.instantiate(cfg.policy)
        self.ema_model: DiffusionTransformerHybridImagePolicy | None = None
        if cfg.training.use_ema:
            self.ema_model = copy.deepcopy(self.model)

        self.optimizer = self.model.get_optimizer(**cfg.optimizer)
        self.global_step = 0
        self.epoch = 0

    def run(self):
        self._run_scheduled(probe_dataset=True)

    def _pre_train_epoch(self, cfg: OmegaConf) -> None:
        return None

    def _compute_training_loss(self, batch, debug_loss: bool):
        loss = self.model.compute_loss(batch, debug_loss)
        return loss, False

    def _compute_validation_loss(self, batch):
        return self.model.compute_loss(batch)

    def _compute_sample_metrics(self, policy, train_sampling_batch, device):
        batch = dict_apply(train_sampling_batch, lambda x: x.to(device, non_blocking=True))
        obs_dict = batch["obs"]
        gt_action = batch["action"]
        result = policy.predict_action(obs_dict)
        pred_action = result["action_pred"]
        if not policy.past_action_pred:
            pred_action = pred_action[:, policy.n_obs_steps - 1 :]
            gt_action = gt_action[:, policy.n_obs_steps - 1 :]
        return {
            "hsic_action_pred_offline": batch_hsic(pred_action).mean().item(),
            "train_action_mse_error": torch.nn.functional.mse_loss(pred_action, gt_action).item(),
        }
