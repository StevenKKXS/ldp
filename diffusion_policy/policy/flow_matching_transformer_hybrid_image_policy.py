from typing import Dict, Optional

import torch
import torch.nn.functional as F
from einops import reduce

from diffusion_policy.common.pytorch_util import dict_apply
from diffusion_policy.policy.diffusion_transformer_hybrid_image_policy import (
    DiffusionTransformerHybridImagePolicy,
)


class FlowMatchingTransformerHybridImagePolicy(DiffusionTransformerHybridImagePolicy):
    """Transformer image policy trained with action-space flow matching.

    This policy intentionally reuses DiffusionTransformerHybridImagePolicy's
    observation encoder, normalizer, optimizer groups, and action slicing
    semantics. The only behavioral difference is the generative objective:

        x_t = t * noise + (1 - t) * action
        target velocity = noise - action

    Inference integrates the learned velocity field from t=1 noise to t=0
    action with a fixed-step Euler solver.
    """

    def __init__(
            self,
            *args,
            num_flow_steps: int = 10,
            time_scale: float = 100.0,
            time_sampling: str = "uniform",
            **kwargs):
        super().__init__(*args, **kwargs)
        if num_flow_steps <= 0:
            raise ValueError(f"num_flow_steps must be > 0, got {num_flow_steps}")
        self.num_flow_steps = int(num_flow_steps)
        self.time_scale = float(time_scale)
        self.time_sampling = str(time_sampling)

    def _sample_time(self, batch_size: int, device: torch.device) -> torch.Tensor:
        if self.time_sampling == "uniform":
            t = torch.rand(batch_size, device=device)
        elif self.time_sampling == "beta_1p5_1":
            dist = torch.distributions.Beta(
                torch.tensor(1.5, device=device),
                torch.tensor(1.0, device=device),
            )
            t = dist.sample((batch_size,))
        else:
            raise ValueError(f"Unsupported time_sampling={self.time_sampling}")
        return t.clamp_(1e-4, 1.0 - 1e-4)

    def _model_time(self, t: torch.Tensor) -> torch.Tensor:
        return t * self.time_scale

    # ========= inference ============
    def conditional_sample(
            self,
            condition_data,
            condition_mask,
            cond=None,
            generator=None,
            act=None,
            **kwargs):
        del kwargs

        trajectory = torch.randn(
            size=condition_data.shape,
            dtype=condition_data.dtype,
            device=condition_data.device,
            generator=generator,
        )

        dt = -1.0 / float(self.num_flow_steps)
        for step in range(self.num_flow_steps):
            time_value = 1.0 + step * dt
            time = torch.full(
                (trajectory.shape[0],),
                fill_value=time_value,
                device=trajectory.device,
                dtype=trajectory.dtype,
            )

            trajectory[condition_mask] = condition_data[condition_mask]
            if act is not None:
                trajectory[:, :act.shape[1]] = act

            velocity = self.model(trajectory, self._model_time(time), cond)
            trajectory = trajectory + dt * velocity

        trajectory[condition_mask] = condition_data[condition_mask]
        if act is not None:
            trajectory[:, :act.shape[1]] = act
        return trajectory

    # ========= training ============
    def compute_loss(self, batch, debug=False):
        del debug

        assert 'valid_mask' not in batch
        nobs = self.normalizer.normalize(batch['obs'])
        nactions = self.normalizer['action'].normalize(batch['action'])
        batch_size = nactions.shape[0]
        horizon = nactions.shape[1]
        To = self.n_obs_steps

        cond = None
        trajectory = nactions
        if self.obs_as_cond:
            if self.use_embed_if_present and "embedding" in batch["obs"]:
                cond = batch["obs"]["embedding"]
            else:
                this_nobs = dict_apply(
                    nobs,
                    lambda x: x[:, :To, ...].reshape(-1, *x.shape[2:]),
                )
                nobs_features = self.obs_encoder(this_nobs)
                cond = nobs_features.reshape(batch_size, To, -1)
            if self.pred_action_steps_only:
                start = To - 1
                end = start + self.n_action_steps
                trajectory = nactions[:, start:end]
        else:
            this_nobs = dict_apply(nobs, lambda x: x.reshape(-1, *x.shape[2:]))
            nobs_features = self.obs_encoder(this_nobs)
            nobs_features = nobs_features.reshape(batch_size, horizon, -1)
            trajectory = torch.cat([nactions, nobs_features], dim=-1).detach()

        if self.pred_action_steps_only:
            condition_mask = torch.zeros_like(trajectory, dtype=torch.bool)
        else:
            condition_mask = self.mask_generator(trajectory.shape)

        noise = torch.randn_like(trajectory)
        t = self._sample_time(trajectory.shape[0], trajectory.device).to(trajectory.dtype)
        t_expanded = t.reshape(-1, *([1] * (trajectory.ndim - 1)))
        noisy_trajectory = t_expanded * noise + (1.0 - t_expanded) * trajectory

        loss_mask = ~condition_mask
        noisy_trajectory[condition_mask] = trajectory[condition_mask]

        pred = self.model(noisy_trajectory, self._model_time(t), cond)
        target = noise - trajectory

        if (not self.pred_action_steps_only) and (not self.past_action_pred):
            pred = pred[:, self.n_obs_steps - 1:]
            target = target[:, self.n_obs_steps - 1:]
            loss_mask = loss_mask[:, self.n_obs_steps - 1:]

        if (not self.pred_action_steps_only) and (self.past_steps_reg != -1):
            assert self.n_obs_steps - self.past_steps_reg - 1 > 0
            start = self.n_obs_steps - self.past_steps_reg - 1
            pred = pred[:, start:]
            target = target[:, start:]
            loss_mask = loss_mask[:, start:]

        loss = F.mse_loss(pred, target, reduction='none')
        loss = loss * loss_mask.type(loss.dtype)
        loss = reduce(loss, 'b ... -> b (...)', 'mean')
        return loss.mean()
