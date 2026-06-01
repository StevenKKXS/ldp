from typing import Dict, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from diffusion_policy.common.pytorch_util import dict_apply, replace_submodules
from diffusion_policy.common.robomimic_config_util import get_robomimic_config
from diffusion_policy.model.common.normalizer import LinearNormalizer
from diffusion_policy.policy.base_image_policy import BaseImagePolicy
from robomimic.algo import algo_factory
from robomimic.algo.algo import PolicyAlgo
import robomimic.models.base_nets as rmbn
try:
    import robomimic.models.obs_core as rmoc
except ImportError:
    rmoc = None
import robomimic.utils.obs_utils as ObsUtils

import diffusion_policy.model.vision.crop_randomizer as dmvc


RobomimicCropRandomizer = getattr(rmbn, "CropRandomizer", None)
if RobomimicCropRandomizer is None and rmoc is not None:
    RobomimicCropRandomizer = getattr(rmoc, "CropRandomizer", None)


def kl_divergence(mu: torch.Tensor, logvar: torch.Tensor) -> torch.Tensor:
    klds = -0.5 * (1 + logvar - mu.pow(2) - logvar.exp())
    return klds.sum(dim=-1).mean()


class OfficialActCore(nn.Module):
    """Robomimic-compatible ACT core with the official CVAE training path.

    The image/proprio encoder is provided by robomimic outside this module. The
    action posterior encoder, latent bottleneck, action queries, decoder depth,
    and KL+L1 objective follow the official ACT design while allowing dynamic
    robomimic action and proprio dimensions.
    """

    def __init__(
            self,
            obs_dim: int,
            qpos_dim: int,
            action_dim: int,
            n_obs_steps: int,
            n_action_steps: int,
            hidden_dim: int = 512,
            enc_layers: int = 4,
            dec_layers: int = 7,
            nheads: int = 8,
            dim_feedforward: int = 3200,
            dropout: float = 0.1,
            latent_dim: int = 32):
        super().__init__()
        self.obs_dim = int(obs_dim)
        self.qpos_dim = int(qpos_dim)
        self.action_dim = int(action_dim)
        self.n_obs_steps = int(n_obs_steps)
        self.n_action_steps = int(n_action_steps)
        self.hidden_dim = int(hidden_dim)
        self.latent_dim = int(latent_dim)

        self.cls_embed = nn.Embedding(1, self.hidden_dim)
        self.posterior_action_proj = nn.Linear(self.action_dim, self.hidden_dim)
        self.posterior_qpos_proj = nn.Linear(self.qpos_dim, self.hidden_dim)
        self.posterior_pos_emb = nn.Parameter(
            torch.zeros(1, 2 + self.n_action_steps, self.hidden_dim))
        posterior_layer = nn.TransformerEncoderLayer(
            d_model=self.hidden_dim,
            nhead=int(nheads),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            activation="relu",
            batch_first=True,
            norm_first=False)
        self.posterior_encoder = nn.TransformerEncoder(
            posterior_layer, num_layers=int(enc_layers))
        self.latent_proj = nn.Linear(self.hidden_dim, self.latent_dim * 2)
        self.latent_out_proj = nn.Linear(self.latent_dim, self.hidden_dim)

        self.obs_proj = nn.Linear(self.obs_dim, self.hidden_dim)
        self.qpos_proj = nn.Linear(self.qpos_dim, self.hidden_dim)
        self.obs_pos_emb = nn.Parameter(
            torch.zeros(1, self.n_obs_steps, self.hidden_dim))
        self.special_pos_emb = nn.Embedding(2, self.hidden_dim)
        memory_layer = nn.TransformerEncoderLayer(
            d_model=self.hidden_dim,
            nhead=int(nheads),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            activation="relu",
            batch_first=True,
            norm_first=False)
        self.memory_encoder = nn.TransformerEncoder(
            memory_layer, num_layers=int(enc_layers))

        self.query_embed = nn.Embedding(self.n_action_steps, self.hidden_dim)
        decoder_layer = nn.TransformerDecoderLayer(
            d_model=self.hidden_dim,
            nhead=int(nheads),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            activation="relu",
            batch_first=True,
            norm_first=False)
        self.decoder = nn.TransformerDecoder(
            decoder_layer, num_layers=int(dec_layers))
        self.action_head = nn.Linear(self.hidden_dim, self.action_dim)
        self.is_pad_head = nn.Linear(self.hidden_dim, 1)

        self._init_parameters()

    def _init_parameters(self):
        nn.init.normal_(self.posterior_pos_emb, mean=0.0, std=0.02)
        nn.init.normal_(self.obs_pos_emb, mean=0.0, std=0.02)

    def _posterior(
            self,
            qpos: torch.Tensor,
            actions: torch.Tensor,
            is_pad: torch.Tensor = None
        ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        bsz = qpos.shape[0]
        cls = self.cls_embed.weight.unsqueeze(0).expand(bsz, -1, -1)
        qpos_token = self.posterior_qpos_proj(qpos).unsqueeze(1)
        action_tokens = self.posterior_action_proj(actions)
        tokens = torch.cat([cls, qpos_token, action_tokens], dim=1)
        tokens = tokens + self.posterior_pos_emb[:, :tokens.shape[1]]
        key_padding_mask = None
        if is_pad is not None:
            prefix = torch.zeros(
                bsz, 2, dtype=torch.bool, device=is_pad.device)
            key_padding_mask = torch.cat([prefix, is_pad.bool()], dim=1)
        hidden = self.posterior_encoder(
            tokens, src_key_padding_mask=key_padding_mask)
        latent_info = self.latent_proj(hidden[:, 0])
        mu, logvar = latent_info.chunk(2, dim=-1)
        std = torch.exp(0.5 * logvar)
        latent_sample = mu + std * torch.randn_like(std)
        return latent_sample, mu, logvar

    def forward(
            self,
            obs_tokens: torch.Tensor,
            qpos: torch.Tensor,
            actions: torch.Tensor = None,
            is_pad: torch.Tensor = None
        ) -> Tuple[torch.Tensor, torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        bsz, horizon, _ = obs_tokens.shape
        if horizon != self.n_obs_steps:
            raise ValueError(f"Expected {self.n_obs_steps} obs steps, got {horizon}.")

        if actions is not None:
            latent_sample, mu, logvar = self._posterior(qpos, actions, is_pad)
        else:
            mu = logvar = None
            latent_sample = torch.zeros(
                bsz, self.latent_dim, dtype=obs_tokens.dtype,
                device=obs_tokens.device)
        latent_token = self.latent_out_proj(latent_sample).unsqueeze(1)
        qpos_token = self.qpos_proj(qpos).unsqueeze(1)
        obs_hidden = self.obs_proj(obs_tokens) + self.obs_pos_emb[:, :horizon]
        special_pos = self.special_pos_emb.weight.unsqueeze(0)
        special = torch.cat([latent_token, qpos_token], dim=1) + special_pos
        memory = torch.cat([obs_hidden, special], dim=1)
        memory = self.memory_encoder(memory)

        queries = self.query_embed.weight.unsqueeze(0).expand(bsz, -1, -1)
        hidden = self.decoder(tgt=queries, memory=memory)
        action = self.action_head(hidden)
        is_pad_hat = self.is_pad_head(hidden).squeeze(-1)
        return action, is_pad_hat, (mu, logvar)


class OfficialActHybridImagePolicy(BaseImagePolicy):
    """ACT CVAE policy adapted to local robomimic image datasets."""

    def __init__(
            self,
            shape_meta: dict,
            horizon,
            n_action_steps,
            n_obs_steps,
            use_embed_if_present=True,
            crop_shape=(76, 76),
            obs_encoder_group_norm=False,
            eval_fixed_crop=False,
            hidden_dim=512,
            enc_layers=4,
            dec_layers=7,
            nheads=8,
            dim_feedforward=3200,
            dropout=0.1,
            latent_dim=32,
            kl_weight=10.0,
            loss_reduction="official_mean",
            temporal_agg=False,
            obs_encoder_freeze=False,
            **kwargs):
        super().__init__()
        self.horizon = int(horizon)
        self.n_action_steps = int(n_action_steps)
        self.n_obs_steps = int(n_obs_steps)
        self.use_embed_if_present = bool(use_embed_if_present)
        self.kl_weight = float(kl_weight)
        self.loss_reduction = str(loss_reduction)
        self.temporal_agg = bool(temporal_agg)
        self.pred_action_steps_only = False
        self.past_action_pred = False

        action_shape = shape_meta["action"]["shape"]
        assert len(action_shape) == 1
        action_dim = int(action_shape[0])
        obs_shape_meta = shape_meta["obs"]
        obs_config = {
            "low_dim": [],
            "rgb": [],
            "depth": [],
            "scan": [],
        }
        obs_key_shapes = dict()
        self.lowdim_keys = []
        for key, attr in obs_shape_meta.items():
            shape = attr["shape"]
            obs_key_shapes[key] = list(shape)
            obs_type = attr.get("type", "low_dim")
            if obs_type == "rgb":
                obs_config["rgb"].append(key)
            elif obs_type == "low_dim":
                obs_config["low_dim"].append(key)
                self.lowdim_keys.append(key)
            else:
                raise RuntimeError(f"Unsupported obs type: {obs_type}")
        qpos_dim = sum(int(torch.prod(torch.tensor(obs_shape_meta[k]["shape"])))
                       for k in self.lowdim_keys)

        config = get_robomimic_config(
            algo_name="bc_rnn",
            hdf5_type="image",
            task_name="square",
            dataset_type="ph")
        with config.unlocked():
            config.observation.modalities.obs = obs_config
            if crop_shape is None:
                for _, modality in config.observation.encoder.items():
                    if modality.obs_randomizer_class == "CropRandomizer":
                        modality["obs_randomizer_class"] = None
            else:
                crop_h, crop_w = crop_shape
                for _, modality in config.observation.encoder.items():
                    if modality.obs_randomizer_class == "CropRandomizer":
                        modality.obs_randomizer_kwargs.crop_height = crop_h
                        modality.obs_randomizer_kwargs.crop_width = crop_w

        ObsUtils.initialize_obs_utils_with_config(config)
        policy: PolicyAlgo = algo_factory(
            algo_name=config.algo_name,
            config=config,
            obs_key_shapes=obs_key_shapes,
            ac_dim=action_dim,
            device="cpu")
        obs_encoder = policy.nets["policy"].nets["encoder"].nets["obs"]

        if obs_encoder_group_norm:
            replace_submodules(
                root_module=obs_encoder,
                predicate=lambda x: isinstance(x, nn.BatchNorm2d),
                func=lambda x: nn.GroupNorm(
                    num_groups=x.num_features // 16,
                    num_channels=x.num_features))
        if eval_fixed_crop:
            replace_submodules(
                root_module=obs_encoder,
                predicate=lambda x: (
                    RobomimicCropRandomizer is not None
                    and isinstance(x, RobomimicCropRandomizer)
                ),
                func=lambda x: dmvc.CropRandomizer(
                    input_shape=x.input_shape,
                    crop_height=x.crop_height,
                    crop_width=x.crop_width,
                    num_crops=x.num_crops,
                    pos_enc=x.pos_enc))

        obs_feature_dim = int(obs_encoder.output_shape()[0])
        self.obs_encoder = obs_encoder
        self.model = OfficialActCore(
            obs_dim=obs_feature_dim,
            qpos_dim=qpos_dim,
            action_dim=action_dim,
            n_obs_steps=self.n_obs_steps,
            n_action_steps=self.n_action_steps,
            hidden_dim=int(hidden_dim),
            enc_layers=int(enc_layers),
            dec_layers=int(dec_layers),
            nheads=int(nheads),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            latent_dim=int(latent_dim))
        self.normalizer = LinearNormalizer()
        self.obs_feature_dim = obs_feature_dim
        self.action_dim = action_dim
        self.qpos_dim = qpos_dim

        if obs_encoder_freeze:
            self.obs_encoder.requires_grad_(False)

    def _encode_obs(self, obs_dict: Dict[str, torch.Tensor]) -> Tuple[torch.Tensor, torch.Tensor]:
        nobs = self.normalizer.normalize(obs_dict)
        value = next(iter(nobs.values()))
        bsz = value.shape[0]
        if self.use_embed_if_present and "embedding" in obs_dict:
            obs_tokens = obs_dict["embedding"][:, :self.n_obs_steps]
        else:
            this_nobs = dict_apply(
                nobs,
                lambda x: x[:, :self.n_obs_steps, ...].reshape(-1, *x.shape[2:]))
            obs_features = self.obs_encoder(this_nobs)
            obs_tokens = obs_features.reshape(bsz, self.n_obs_steps, -1)

        qpos_parts = []
        for key in self.lowdim_keys:
            qpos_parts.append(nobs[key][:, self.n_obs_steps - 1].reshape(bsz, -1))
        qpos = torch.cat(qpos_parts, dim=-1)
        return obs_tokens, qpos

    def _target_action(self, action: torch.Tensor) -> torch.Tensor:
        start = self.n_obs_steps - 1
        end = start + self.n_action_steps
        return action[:, start:end]

    def _l1_loss(
            self,
            pred: torch.Tensor,
            target: torch.Tensor,
            is_pad: torch.Tensor
        ) -> torch.Tensor:
        all_l1 = F.l1_loss(pred, target, reduction="none")
        valid = (~is_pad.bool()).unsqueeze(-1).to(all_l1.dtype)
        if self.loss_reduction == "official_mean":
            return (all_l1 * valid).mean()
        if self.loss_reduction == "sum_action_dim":
            per_step = (all_l1 * valid).sum(dim=-1)
            denom = valid.squeeze(-1).sum().clamp_min(1.0)
            return per_step.sum() / denom
        raise ValueError(f"Unsupported loss_reduction: {self.loss_reduction}")

    def predict_action(self, obs_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        obs_tokens, qpos = self._encode_obs(obs_dict)
        naction_pred, _, _ = self.model(obs_tokens, qpos)
        naction_full = torch.zeros(
            naction_pred.shape[0],
            self.horizon,
            self.action_dim,
            dtype=naction_pred.dtype,
            device=naction_pred.device)
        start = self.n_obs_steps - 1
        end = start + self.n_action_steps
        naction_full[:, start:end] = naction_pred
        action_pred = self.normalizer["action"].unnormalize(naction_full)
        action = action_pred[:, start:end]
        return {
            "action": action,
            "action_pred": action_pred,
        }

    def set_normalizer(self, normalizer: LinearNormalizer):
        self.normalizer.load_state_dict(normalizer.state_dict())

    def get_optimizer(
            self,
            transformer_weight_decay: float,
            obs_encoder_weight_decay: float,
            learning_rate: float,
            betas: Tuple[float, float]) -> torch.optim.Optimizer:
        optimizer = torch.optim.AdamW(
            [
                {
                    "params": self.model.parameters(),
                    "weight_decay": transformer_weight_decay,
                },
                {
                    "params": self.obs_encoder.parameters(),
                    "weight_decay": obs_encoder_weight_decay,
                },
            ],
            lr=learning_rate,
            betas=betas)
        return optimizer

    def compute_loss(self, batch, debug=False):
        obs_tokens, qpos = self._encode_obs(batch["obs"])
        nactions = self.normalizer["action"].normalize(batch["action"])
        target = self._target_action(nactions)
        is_pad = torch.zeros(
            target.shape[:2], dtype=torch.bool, device=target.device)
        naction_pred, _, (mu, logvar) = self.model(
            obs_tokens, qpos, actions=target, is_pad=is_pad)
        l1 = self._l1_loss(naction_pred, target, is_pad)
        kl = kl_divergence(mu, logvar)
        return l1 + self.kl_weight * kl
