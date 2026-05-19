from typing import Dict

import torch
import torch.nn as nn


class BehaviorTranslator(nn.Module):
    def __init__(
            self,
            obs_dim: int,
            action_dim: int,
            obs_horizon: int,
            past_action_horizon: int,
            future_action_horizon: int,
            d_model: int = 256,
            n_encoder_layers: int = 4,
            n_decoder_layers: int = 2,
            n_heads: int = 4,
            ff_dim: int = 1024,
            dropout: float = 0.1,
            context_dim: int = 512,
            causal_obs_encoder: bool = True,
            context_mode: str = "concat_obs_action_pool"):
        super().__init__()
        self.obs_dim = int(obs_dim)
        self.action_dim = int(action_dim)
        self.obs_horizon = int(obs_horizon)
        self.past_action_horizon = int(past_action_horizon)
        self.future_action_horizon = int(future_action_horizon)
        self.d_model = int(d_model)
        self.context_dim = int(context_dim)
        self.causal_obs_encoder = bool(causal_obs_encoder)
        self.context_mode = context_mode

        n_action_queries = self.past_action_horizon + self.future_action_horizon
        assert n_action_queries > 0

        self.obs_projector = nn.Linear(self.obs_dim, self.d_model)
        self.obs_pos_emb = nn.Parameter(torch.zeros(1, self.obs_horizon, self.d_model))
        self.action_queries = nn.Parameter(torch.zeros(1, n_action_queries, self.d_model))

        enc_layer = nn.TransformerEncoderLayer(
            d_model=self.d_model,
            nhead=n_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
            norm_first=True)
        self.obs_encoder = nn.TransformerEncoder(enc_layer, num_layers=n_encoder_layers)

        dec_layer = nn.TransformerDecoderLayer(
            d_model=self.d_model,
            nhead=n_heads,
            dim_feedforward=ff_dim,
            dropout=dropout,
            batch_first=True,
            norm_first=True)
        self.action_decoder = nn.TransformerDecoder(dec_layer, num_layers=n_decoder_layers)

        self.sketch_action_head = nn.Sequential(
            nn.LayerNorm(self.d_model),
            nn.Linear(self.d_model, self.d_model),
            nn.GELU(),
            nn.Linear(self.d_model, self.action_dim),
        )
        self.context_projector = nn.Sequential(
            nn.LayerNorm(self.d_model * 3),
            nn.Linear(self.d_model * 3, self.context_dim),
        )

        self._init_parameters()

    def _init_parameters(self):
        nn.init.normal_(self.obs_pos_emb, mean=0.0, std=0.02)
        nn.init.normal_(self.action_queries, mean=0.0, std=0.02)

    def _causal_mask(self, length: int, device):
        return torch.triu(
            torch.ones(length, length, device=device, dtype=torch.bool),
            diagonal=1)

    def _build_context(self, z_obs: torch.Tensor, h_action: torch.Tensor):
        p = self.past_action_horizon
        if self.future_action_horizon > 0:
            h_future = h_action[:, p:, :]
        else:
            h_future = h_action
        h_future_pool = h_future.mean(dim=1)
        h_all_pool = h_action.mean(dim=1)
        z_last = z_obs[:, -1, :]
        return self.context_projector(torch.cat([h_future_pool, h_all_pool, z_last], dim=-1))

    def forward(self, obs_tokens: torch.Tensor, return_context: bool = True) -> Dict[str, torch.Tensor]:
        assert obs_tokens.ndim == 3
        bsz, horizon, obs_dim = obs_tokens.shape
        assert horizon == self.obs_horizon, (horizon, self.obs_horizon)
        assert obs_dim == self.obs_dim, (obs_dim, self.obs_dim)

        z = self.obs_projector(obs_tokens) + self.obs_pos_emb[:, :horizon]
        src_mask = None
        if self.causal_obs_encoder:
            src_mask = self._causal_mask(horizon, obs_tokens.device)
        z_obs = self.obs_encoder(z, mask=src_mask)

        queries = self.action_queries.expand(bsz, -1, -1)
        h_action = self.action_decoder(tgt=queries, memory=z_obs)
        pred_actions = self.sketch_action_head(h_action)

        result = {
            "pred_actions": pred_actions,
            "context_tokens": h_action,
            "z_obs": z_obs,
        }
        if return_context:
            result["context"] = self._build_context(z_obs, h_action)
        return result

    def get_context(self, obs_tokens: torch.Tensor) -> torch.Tensor:
        return self.forward(obs_tokens, return_context=True)["context"]
