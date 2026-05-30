from typing import Dict, Optional, Tuple
import copy
import dill
import pathlib

import torch
import torch.nn as nn

from diffusion_policy.common.pytorch_util import dict_apply
from diffusion_policy.model.behavior_translator import BehaviorTranslator
from diffusion_policy.policy.diffusion_transformer_hybrid_image_policy import (
    DiffusionTransformerHybridImagePolicy,
)


class TranslatorConditionedTransformerHybridImagePolicy(DiffusionTransformerHybridImagePolicy):
    def __init__(
            self,
            *args,
            translator_checkpoint: Optional[str] = None,
            translator_context_source: str = "checkpoint",
            translator_obs_horizon: int = 16,
            translator_past_action_horizon: int = 16,
            translator_future_action_horizon: int = 8,
            translator_d_model: int = 256,
            translator_n_encoder_layers: int = 4,
            translator_n_decoder_layers: int = 2,
            translator_n_heads: int = 4,
            translator_ff_dim: int = 1024,
            translator_dropout: float = 0.1,
            translator_context_dim: int = 512,
            translator_causal_obs_encoder: bool = True,
            translator_freeze: bool = True,
            context_injection: str = "add_all",
            context_projector_zero_init: bool = True,
            translator_context_norm: bool = False,
            **kwargs):
        super().__init__(*args, **kwargs)

        self.translator_obs_horizon = int(translator_obs_horizon)
        self.translator_freeze = bool(translator_freeze)
        self.translator_context_source = str(translator_context_source)
        self.context_injection = str(context_injection)
        self.translator_context_norm_enabled = bool(translator_context_norm)

        self.translator_obs_encoder = copy.deepcopy(self.obs_encoder)
        self.translator_model = BehaviorTranslator(
            obs_dim=int(self.obs_feature_dim),
            action_dim=int(self.action_dim),
            obs_horizon=self.translator_obs_horizon,
            past_action_horizon=int(translator_past_action_horizon),
            future_action_horizon=int(translator_future_action_horizon),
            d_model=int(translator_d_model),
            n_encoder_layers=int(translator_n_encoder_layers),
            n_decoder_layers=int(translator_n_decoder_layers),
            n_heads=int(translator_n_heads),
            ff_dim=int(translator_ff_dim),
            dropout=float(translator_dropout),
            context_dim=int(translator_context_dim),
            causal_obs_encoder=bool(translator_causal_obs_encoder),
        )
        self.translator_context_norm = (
            nn.LayerNorm(int(translator_context_dim))
            if self.translator_context_norm_enabled
            else nn.Identity()
        )
        self.translator_context_projector = nn.Linear(
            int(translator_context_dim), int(self.obs_feature_dim))

        if bool(context_projector_zero_init):
            nn.init.zeros_(self.translator_context_projector.weight)
            nn.init.zeros_(self.translator_context_projector.bias)

        if self.translator_context_source == "checkpoint":
            if translator_checkpoint is None or str(translator_checkpoint) == "":
                raise ValueError(
                    "translator_checkpoint is required when "
                    "translator_context_source=checkpoint")
            self._load_translator_checkpoint(translator_checkpoint)
        elif self.translator_context_source == "random":
            pass
        else:
            raise ValueError(
                f"Unsupported translator_context_source: "
                f"{self.translator_context_source}")

        if self.translator_freeze:
            self.translator_obs_encoder.requires_grad_(False)
            self.translator_model.requires_grad_(False)
            self.translator_obs_encoder.eval()
            self.translator_model.eval()

    def _load_translator_checkpoint(self, path):
        path = pathlib.Path(path)
        payload = torch.load(path.open("rb"), pickle_module=dill, map_location="cpu")
        self.translator_obs_encoder.load_state_dict(
            payload["state_dicts"]["obs_encoder"])
        self.translator_model.load_state_dict(payload["state_dicts"]["model"])
        return payload

    def train(self, mode: bool = True):
        result = super().train(mode)
        if self.translator_freeze:
            self.translator_obs_encoder.eval()
            self.translator_model.eval()
        return result

    def get_optimizer(
            self,
            transformer_weight_decay: float,
            obs_encoder_weight_decay: float,
            learning_rate: float,
            betas: Tuple[float, float]
        ) -> torch.optim.Optimizer:
        optim_groups = self.model.get_optim_groups(
            weight_decay=transformer_weight_decay)
        optim_groups.append({
            "params": self.obs_encoder.parameters(),
            "weight_decay": obs_encoder_weight_decay
        })
        optim_groups.append({
            "params": list(self.translator_context_norm.parameters())
            + list(self.translator_context_projector.parameters()),
            "weight_decay": transformer_weight_decay
        })
        if not self.translator_freeze:
            optim_groups.append({
                "params": self.translator_obs_encoder.parameters(),
                "weight_decay": obs_encoder_weight_decay
            })
            optim_groups.append({
                "params": self.translator_model.parameters(),
                "weight_decay": transformer_weight_decay
            })
        optimizer = torch.optim.AdamW(
            optim_groups, lr=learning_rate, betas=betas
        )
        return optimizer

    def _compute_translator_context(self, nobs: Dict[str, torch.Tensor]) -> torch.Tensor:
        value = next(iter(nobs.values()))
        bsz, horizon = value.shape[:2]
        if horizon < self.translator_obs_horizon:
            raise ValueError(
                f"Translator requires at least {self.translator_obs_horizon} "
                f"obs steps, but got {horizon}. Increase n_obs_steps.")

        translator_nobs = dict_apply(
            nobs,
            lambda x: x[:, -self.translator_obs_horizon:, ...].reshape(
                bsz * self.translator_obs_horizon, *x.shape[2:]))
        obs_tokens = self.translator_obs_encoder(translator_nobs).reshape(
            bsz, self.translator_obs_horizon, -1)
        return self.translator_model.get_context(obs_tokens)

    def _augment_condition(
            self,
            cond: torch.Tensor,
            nobs: Optional[Dict[str, torch.Tensor]] = None,
            raw_obs: Optional[Dict[str, torch.Tensor]] = None
        ) -> torch.Tensor:
        if nobs is None:
            return cond
        grad_enabled = not self.translator_freeze
        with torch.set_grad_enabled(grad_enabled):
            context = self._compute_translator_context(nobs)
        context = context.detach() if self.translator_freeze else context
        context = self.translator_context_norm(context)
        context_token = self.translator_context_projector(context)

        if self.context_injection == "add_all":
            return cond + context_token.unsqueeze(1)
        if self.context_injection == "add_last":
            result = cond.clone()
            result[:, -1, :] = result[:, -1, :] + context_token
            return result
        raise ValueError(f"Unsupported context_injection: {self.context_injection}")
