from typing import Dict, Tuple
import copy

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


class ActionChunkingTransformer(nn.Module):
    """Minimal ACT-style action chunk decoder over encoded observation history."""

    def __init__(
            self,
            obs_dim: int,
            action_dim: int,
            n_obs_steps: int,
            n_action_steps: int,
            hidden_dim: int = 512,
            n_encoder_layers: int = 4,
            n_decoder_layers: int = 7,
            n_head: int = 8,
            dim_feedforward: int = 3200,
            dropout: float = 0.1,
            causal_obs_encoder: bool = False):
        super().__init__()
        self.n_obs_steps = int(n_obs_steps)
        self.n_action_steps = int(n_action_steps)
        self.hidden_dim = int(hidden_dim)
        self.causal_obs_encoder = bool(causal_obs_encoder)

        self.obs_proj = nn.Linear(int(obs_dim), self.hidden_dim)
        self.obs_pos_emb = nn.Parameter(torch.zeros(1, self.n_obs_steps, self.hidden_dim))
        self.action_queries = nn.Parameter(torch.zeros(1, self.n_action_steps, self.hidden_dim))

        enc_layer = nn.TransformerEncoderLayer(
            d_model=self.hidden_dim,
            nhead=int(n_head),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            activation="gelu",
            batch_first=True,
            norm_first=True)
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=int(n_encoder_layers))

        dec_layer = nn.TransformerDecoderLayer(
            d_model=self.hidden_dim,
            nhead=int(n_head),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            activation="gelu",
            batch_first=True,
            norm_first=True)
        self.decoder = nn.TransformerDecoder(dec_layer, num_layers=int(n_decoder_layers))
        self.head = nn.Sequential(
            nn.LayerNorm(self.hidden_dim),
            nn.Linear(self.hidden_dim, int(action_dim)),
        )
        self.apply(self._init_weights)
        nn.init.normal_(self.obs_pos_emb, mean=0.0, std=0.02)
        nn.init.normal_(self.action_queries, mean=0.0, std=0.02)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.LayerNorm):
            nn.init.ones_(module.weight)
            nn.init.zeros_(module.bias)

    def _causal_mask(self, length: int, device):
        return torch.triu(
            torch.ones(length, length, device=device, dtype=torch.bool),
            diagonal=1)

    def forward(self, obs_tokens: torch.Tensor) -> torch.Tensor:
        bsz, horizon, _ = obs_tokens.shape
        if horizon != self.n_obs_steps:
            raise ValueError(f"Expected {self.n_obs_steps} obs steps, got {horizon}.")
        x = self.obs_proj(obs_tokens) + self.obs_pos_emb[:, :horizon]
        mask = self._causal_mask(horizon, obs_tokens.device) if self.causal_obs_encoder else None
        memory = self.encoder(x, mask=mask)
        queries = self.action_queries.expand(bsz, -1, -1)
        hidden = self.decoder(tgt=queries, memory=memory)
        return self.head(hidden)


class ActionChunkingTransformerHybridImagePolicy(BaseImagePolicy):
    """ACT-style image policy v0.

    This is a deterministic action-chunking Transformer baseline. It matches
    the ACT-scale encoder/decoder geometry used in the plan, but intentionally
    leaves the CVAE latent path out for the first smokeable comparison.
    """

    def __init__(
            self,
            shape_meta: dict,
            horizon,
            n_action_steps,
            n_obs_steps,
            noise_scheduler=None,
            use_embed_if_present=True,
            crop_shape=(76, 76),
            obs_encoder_group_norm=False,
            eval_fixed_crop=False,
            hidden_dim=512,
            n_encoder_layers=4,
            n_decoder_layers=7,
            n_head=8,
            dim_feedforward=3200,
            dropout=0.1,
            causal_obs_encoder=False,
            loss_type="l1",
            loss_scale=1.0,
            loss_reduction="mean",
            pred_action_steps_only=True,
            past_action_pred=False,
            obs_encoder_freeze=False,
            **kwargs):
        super().__init__()
        self.horizon = int(horizon)
        self.n_action_steps = int(n_action_steps)
        self.n_obs_steps = int(n_obs_steps)
        self.use_embed_if_present = bool(use_embed_if_present)
        self.loss_type = str(loss_type)
        self.loss_scale = float(loss_scale)
        self.loss_reduction = str(loss_reduction)
        self.pred_action_steps_only = bool(pred_action_steps_only)
        self.past_action_pred = bool(past_action_pred)

        action_shape = shape_meta["action"]["shape"]
        assert len(action_shape) == 1
        action_dim = action_shape[0]
        obs_shape_meta = shape_meta["obs"]
        obs_config = {
            "low_dim": [],
            "rgb": [],
            "depth": [],
            "scan": [],
        }
        obs_key_shapes = dict()
        for key, attr in obs_shape_meta.items():
            shape = attr["shape"]
            obs_key_shapes[key] = list(shape)
            obs_type = attr.get("type", "low_dim")
            if obs_type == "rgb":
                obs_config["rgb"].append(key)
            elif obs_type == "low_dim":
                obs_config["low_dim"].append(key)
            else:
                raise RuntimeError(f"Unsupported obs type: {obs_type}")

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

        obs_feature_dim = obs_encoder.output_shape()[0]
        self.obs_encoder = obs_encoder
        self.model = ActionChunkingTransformer(
            obs_dim=obs_feature_dim,
            action_dim=action_dim,
            n_obs_steps=self.n_obs_steps,
            n_action_steps=self.n_action_steps,
            hidden_dim=int(hidden_dim),
            n_encoder_layers=int(n_encoder_layers),
            n_decoder_layers=int(n_decoder_layers),
            n_head=int(n_head),
            dim_feedforward=int(dim_feedforward),
            dropout=float(dropout),
            causal_obs_encoder=bool(causal_obs_encoder))
        self.normalizer = LinearNormalizer()
        self.obs_feature_dim = obs_feature_dim
        self.action_dim = action_dim

        if obs_encoder_freeze:
            self.obs_encoder.requires_grad_(False)

    def _encode_obs(self, obs_dict: Dict[str, torch.Tensor]) -> torch.Tensor:
        nobs = self.normalizer.normalize(obs_dict)
        if self.use_embed_if_present and "embedding" in obs_dict:
            return obs_dict["embedding"][:, :self.n_obs_steps]
        value = next(iter(nobs.values()))
        bsz = value.shape[0]
        this_nobs = dict_apply(
            nobs,
            lambda x: x[:, :self.n_obs_steps, ...].reshape(-1, *x.shape[2:]))
        obs_features = self.obs_encoder(this_nobs)
        return obs_features.reshape(bsz, self.n_obs_steps, -1)

    def _target_action(self, action: torch.Tensor) -> torch.Tensor:
        start = self.n_obs_steps - 1
        end = start + self.n_action_steps
        return action[:, start:end]

    def _loss(self, pred: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        if self.loss_type == "l1":
            loss = F.l1_loss(pred, target, reduction="none")
        elif self.loss_type == "smooth_l1":
            loss = F.smooth_l1_loss(pred, target, reduction="none")
        elif self.loss_type == "mse":
            loss = F.mse_loss(pred, target, reduction="none")
        else:
            raise ValueError(f"Unsupported loss_type: {self.loss_type}")

        if self.loss_reduction == "mean":
            loss = loss.mean()
        elif self.loss_reduction == "sum_action_dim":
            loss = loss.sum(dim=-1).mean()
        else:
            raise ValueError(f"Unsupported loss_reduction: {self.loss_reduction}")
        return loss * self.loss_scale

    def predict_action(self, obs_dict: Dict[str, torch.Tensor]) -> Dict[str, torch.Tensor]:
        cond = self._encode_obs(obs_dict)
        naction_pred = self.model(cond)
        action_pred = self.normalizer["action"].unnormalize(naction_pred)
        return {
            "action": action_pred,
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
        obs_tokens = self._encode_obs(batch["obs"])
        naction_pred = self.model(obs_tokens)
        nactions = self.normalizer["action"].normalize(batch["action"])
        target = self._target_action(nactions)
        return self._loss(naction_pred, target)
