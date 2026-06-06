if __name__ == "__main__":
    import os
    import pathlib
    import sys

    ROOT_DIR = str(pathlib.Path(__file__).parent.parent.parent)
    sys.path.append(ROOT_DIR)
    os.chdir(ROOT_DIR)

import copy
import json
import os
import pathlib
import random
from typing import Dict

import dill
import hydra
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import tqdm
from omegaconf import OmegaConf
from torch.utils.data import DataLoader

from diffusion_policy.common.pytorch_util import dict_apply
from diffusion_policy.dataset.base_dataset import BaseImageDataset
from diffusion_policy.workspace.base_workspace import BaseWorkspace

OmegaConf.register_new_resolver("eval", eval, replace=True)


def _copy_to_cpu(value):
    if isinstance(value, torch.Tensor):
        return value.detach().to("cpu")
    if isinstance(value, dict):
        return {k: _copy_to_cpu(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_copy_to_cpu(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_copy_to_cpu(v) for v in value)
    return copy.deepcopy(value)


class EncoderPretrainModel(nn.Module):
    def __init__(
            self,
            obs_encoder: nn.Module,
            obs_feature_dim: int,
            n_obs_steps: int,
            action_dim: int,
            target_steps: int,
            objective: str,
            pooling: str = "flatten",
            hidden_dim: int = 512,
            projection_dim: int = 128,
            dropout: float = 0.0):
        super().__init__()
        self.obs_encoder = obs_encoder
        self.obs_feature_dim = int(obs_feature_dim)
        self.n_obs_steps = int(n_obs_steps)
        self.action_dim = int(action_dim)
        self.target_steps = int(target_steps)
        self.objective = str(objective)
        self.pooling = str(pooling)

        if self.pooling == "flatten":
            pooled_dim = self.n_obs_steps * self.obs_feature_dim
        elif self.pooling in ("mean", "last"):
            pooled_dim = self.obs_feature_dim
        else:
            raise ValueError(f"Unsupported pooling={pooling}")

        if self.objective == "predictive":
            self.head = nn.Sequential(
                nn.Linear(pooled_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.Mish(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim, hidden_dim),
                nn.Mish(),
                nn.Linear(hidden_dim, self.target_steps * self.action_dim),
            )
        elif self.objective == "contrastive":
            self.head = nn.Sequential(
                nn.Linear(pooled_dim, hidden_dim),
                nn.LayerNorm(hidden_dim),
                nn.Mish(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim, projection_dim),
            )
        else:
            raise ValueError(f"Unsupported objective={objective}")

    def encode_obs(self, nobs: Dict[str, torch.Tensor]) -> torch.Tensor:
        value = next(iter(nobs.values()))
        batch_size = value.shape[0]
        to = self.n_obs_steps
        this_nobs = dict_apply(
            nobs,
            lambda x: x[:, :to, ...].reshape(-1, *x.shape[2:]),
        )
        features = self.obs_encoder(this_nobs)
        features = features.reshape(batch_size, to, -1)
        return features

    def pool_features(self, features: torch.Tensor) -> torch.Tensor:
        if self.pooling == "flatten":
            return features.reshape(features.shape[0], -1)
        if self.pooling == "mean":
            return features.mean(dim=1)
        if self.pooling == "last":
            return features[:, -1]
        raise ValueError(f"Unsupported pooling={self.pooling}")

    def forward(self, nobs: Dict[str, torch.Tensor]) -> torch.Tensor:
        features = self.encode_obs(nobs)
        pooled = self.pool_features(features)
        output = self.head(pooled)
        if self.objective == "predictive":
            output = output.reshape(-1, self.target_steps, self.action_dim)
        return output


class TrainEncoderPretrainWorkspace(BaseWorkspace):
    include_keys = ["global_step", "epoch"]

    def __init__(self, cfg: OmegaConf, output_dir=None):
        super().__init__(cfg, output_dir=output_dir)

        seed = cfg.training.seed
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)

        policy = hydra.utils.instantiate(cfg.policy)
        for param in policy.obs_encoder.parameters():
            param.requires_grad = True

        self.model = EncoderPretrainModel(
            obs_encoder=policy.obs_encoder,
            obs_feature_dim=policy.obs_feature_dim,
            n_obs_steps=cfg.n_obs_steps,
            action_dim=policy.action_dim,
            target_steps=self._target_steps_from_cfg(cfg),
            objective=cfg.pretrain.objective,
            pooling=cfg.pretrain.pooling,
            hidden_dim=cfg.pretrain.hidden_dim,
            projection_dim=cfg.pretrain.projection_dim,
            dropout=cfg.pretrain.dropout,
        )
        self.normalizer = None
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=cfg.optimizer.learning_rate,
            betas=tuple(cfg.optimizer.betas),
            weight_decay=cfg.optimizer.weight_decay,
        )
        self.global_step = 0
        self.epoch = 0

    def _target_steps_from_cfg(self, cfg):
        mode = cfg.pretrain.target_mode
        if mode == "full":
            return int(cfg.horizon)
        if mode == "future":
            return int(cfg.n_action_steps)
        if mode == "post_obs":
            return int(cfg.horizon - cfg.n_obs_steps + 1)
        raise ValueError(f"Unsupported target_mode={mode}")

    def _select_action_target(self, nactions: torch.Tensor) -> torch.Tensor:
        mode = self.cfg.pretrain.target_mode
        if mode == "full":
            return nactions
        if mode == "future":
            start = self.cfg.n_obs_steps - 1
            end = start + self.cfg.n_action_steps
            return nactions[:, start:end]
        if mode == "post_obs":
            return nactions[:, self.cfg.n_obs_steps - 1:]
        raise ValueError(f"Unsupported target_mode={mode}")

    def _predictive_loss(self, batch):
        nobs = self.normalizer.normalize(batch["obs"])
        nactions = self.normalizer["action"].normalize(batch["action"])
        target = self._select_action_target(nactions)
        pred = self.model(nobs)
        loss = F.smooth_l1_loss(
            pred,
            target,
            beta=self.cfg.pretrain.huber_beta,
            reduction="none",
        )
        per_timestep = loss.mean(dim=(0, 2))
        per_dim = loss.mean(dim=(0, 1))
        return loss.mean(), {
            "pred_loss": loss.mean().detach(),
            "target_abs_mean": target.abs().mean().detach(),
            "pred_abs_mean": pred.abs().mean().detach(),
            "per_timestep_loss_mean": per_timestep.mean().detach(),
            "per_dim_loss_mean": per_dim.mean().detach(),
        }

    def _contrastive_loss(self, batch):
        nobs = self.normalizer.normalize(batch["obs"])
        nactions = self.normalizer["action"].normalize(batch["action"])
        target = self._select_action_target(nactions)
        z = self.model(nobs)
        z = F.normalize(z, dim=-1)

        flat_action = target.reshape(target.shape[0], -1)
        action_dist = torch.cdist(flat_action, flat_action, p=2)
        diag = torch.eye(action_dist.shape[0], dtype=torch.bool, device=action_dist.device)
        valid_dist = action_dist[~diag]
        if self.cfg.pretrain.sigma <= 0:
            sigma = valid_dist.detach().median().clamp_min(1e-6)
        else:
            sigma = torch.as_tensor(
                float(self.cfg.pretrain.sigma),
                device=action_dist.device,
                dtype=action_dist.dtype,
            )
        logits_q = -action_dist / sigma
        logits_q = logits_q.masked_fill(diag, float("-inf"))
        q = torch.softmax(logits_q, dim=-1).detach()

        sim = torch.matmul(z, z.T) / float(self.cfg.pretrain.tau)
        sim = sim.masked_fill(diag, float("-inf"))
        log_p = torch.log_softmax(sim, dim=-1)
        log_p = log_p.masked_fill(diag, 0.0)
        loss = -(q * log_p).sum(dim=-1).mean()
        return loss, {
            "contrast_loss": loss.detach(),
            "action_dist_median": valid_dist.detach().median(),
            "action_dist_mean": valid_dist.detach().mean(),
            "embedding_abs_mean": z.abs().mean().detach(),
            "embedding_std": z.std(dim=0).mean().detach(),
            "sigma": sigma.detach(),
        }

    def compute_loss(self, batch):
        if self.cfg.pretrain.objective == "predictive":
            return self._predictive_loss(batch)
        if self.cfg.pretrain.objective == "contrastive":
            return self._contrastive_loss(batch)
        raise ValueError(f"Unsupported objective={self.cfg.pretrain.objective}")

    def save_encoder_checkpoint(self, tag="latest"):
        path = pathlib.Path(self.output_dir).joinpath("checkpoints", f"{tag}.ckpt")
        path.parent.mkdir(parents=True, exist_ok=True)
        model_state = {}
        for key, value in self.model.obs_encoder.state_dict().items():
            model_state[f"obs_encoder.{key}"] = value.detach().to("cpu")
        payload = {
            "cfg": self.cfg,
            "state_dicts": {
                "model": model_state,
                "encoder_pretrain_model": _copy_to_cpu(self.model.state_dict()),
                "optimizer": _copy_to_cpu(self.optimizer.state_dict()),
            },
            "pickles": {
                "global_step": dill.dumps(self.global_step),
                "epoch": dill.dumps(self.epoch),
                "_output_dir": dill.dumps(self.output_dir),
            },
        }
        torch.save(payload, path.open("wb"), pickle_module=dill)
        return str(path.absolute())

    def run(self):
        cfg = copy.deepcopy(self.cfg)
        pathlib.Path(self.output_dir).mkdir(parents=True, exist_ok=True)

        dataset = hydra.utils.instantiate(cfg.task.dataset)
        assert isinstance(dataset, BaseImageDataset)
        dataset[0]
        train_dataloader = DataLoader(dataset, **cfg.dataloader)
        val_dataset = dataset.get_validation_dataset()
        val_dataloader = DataLoader(val_dataset, **cfg.val_dataloader)

        self.normalizer = dataset.get_normalizer()
        device = torch.device(cfg.training.device)
        self.normalizer.to(device)
        self.model.to(device)

        log_path = pathlib.Path(self.output_dir).joinpath("logs.jsonl")
        with log_path.open("a") as log_file:
            for _ in range(cfg.training.num_epochs):
                self.model.train()
                train_losses = []
                with tqdm.tqdm(
                        train_dataloader,
                        desc=f"Encoder pretrain epoch {self.epoch}",
                        leave=False,
                        mininterval=cfg.training.tqdm_interval_sec) as tepoch:
                    for batch_idx, batch in enumerate(tepoch):
                        batch = dict_apply(batch, lambda x: x.to(device, non_blocking=True))
                        loss, metrics = self.compute_loss(batch)
                        loss.backward()
                        if (batch_idx + 1) % cfg.training.gradient_accumulate_every == 0:
                            self.optimizer.step()
                            self.optimizer.zero_grad(set_to_none=True)
                        train_losses.append(loss.item())
                        tepoch.set_postfix(loss=loss.item(), refresh=False)
                        self.global_step += 1
                        if cfg.training.max_train_steps is not None and \
                                batch_idx >= cfg.training.max_train_steps - 1:
                            break

                step_log = {
                    "epoch": self.epoch,
                    "global_step": self.global_step,
                    "train_loss": float(np.mean(train_losses)) if train_losses else None,
                }
                step_log.update({
                    f"train_{key}": float(value.detach().cpu())
                    for key, value in metrics.items()
                })

                if self.epoch % cfg.training.val_every == 0:
                    self.model.eval()
                    val_losses = []
                    with torch.no_grad():
                        for batch_idx, batch in enumerate(val_dataloader):
                            batch = dict_apply(batch, lambda x: x.to(device, non_blocking=True))
                            loss, val_metrics = self.compute_loss(batch)
                            val_losses.append(loss.item())
                            if cfg.training.max_val_steps is not None and \
                                    batch_idx >= cfg.training.max_val_steps - 1:
                                break
                    if val_losses:
                        step_log["val_loss"] = float(np.mean(val_losses))
                        step_log.update({
                            f"val_{key}": float(value.detach().cpu())
                            for key, value in val_metrics.items()
                        })

                if (self.epoch + 1) % cfg.training.checkpoint_every == 0:
                    step_log["checkpoint"] = self.save_encoder_checkpoint()
                log_file.write(json.dumps(step_log) + "\n")
                log_file.flush()
                self.epoch += 1

        self.save_encoder_checkpoint()


@hydra.main(
    version_base=None,
    config_path=str(pathlib.Path(__file__).parent.parent.joinpath("config")),
    config_name=pathlib.Path(__file__).stem)
def main(cfg):
    workspace = TrainEncoderPretrainWorkspace(cfg)
    workspace.run()


if __name__ == "__main__":
    main()
