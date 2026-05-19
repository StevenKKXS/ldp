from typing import Dict
import copy

import numpy as np
import torch
from diffusion_policy.common.pytorch_util import dict_apply
from diffusion_policy.dataset.base_dataset import BaseImageDataset


class BehaviorTranslationDataset(BaseImageDataset):
    """Build explicit obs-history to action-window samples for translator pretraining."""

    def __init__(
            self,
            base_dataset: BaseImageDataset,
            obs_horizon: int,
            past_action_horizon: int,
            future_action_horizon: int,
            shuffle_obs_history: bool = False,
            single_frame_obs: bool = False,
            seed: int = 42):
        super().__init__()
        assert obs_horizon >= 1
        assert past_action_horizon >= 0
        assert future_action_horizon >= 1

        self.base_dataset = base_dataset
        self.obs_horizon = int(obs_horizon)
        self.past_action_horizon = int(past_action_horizon)
        self.future_action_horizon = int(future_action_horizon)
        self.shuffle_obs_history = bool(shuffle_obs_history)
        self.single_frame_obs = bool(single_frame_obs)
        self.seed = int(seed)

        self.anchor = max(self.past_action_horizon, self.obs_horizon - 1)
        self.sequence_length = self.anchor + self.future_action_horizon
        if hasattr(base_dataset, "sampler"):
            assert base_dataset.sampler.sequence_length == self.sequence_length, (
                base_dataset.sampler.sequence_length,
                self.sequence_length)

    def get_validation_dataset(self):
        result = copy.copy(self)
        result.base_dataset = self.base_dataset.get_validation_dataset()
        return result

    def get_normalizer(self, **kwargs):
        return self.base_dataset.get_normalizer(**kwargs)

    def get_all_actions(self):
        return self.base_dataset.get_all_actions()

    def __len__(self):
        return len(self.base_dataset.sampler)

    def _sample_obs_indices(self, idx):
        if self.single_frame_obs:
            return np.array([self.anchor], dtype=np.int64)

        obs_start = self.anchor - self.obs_horizon + 1
        obs_end = self.anchor + 1
        obs_indices = np.arange(obs_start, obs_end, dtype=np.int64)
        if self.shuffle_obs_history:
            rng = np.random.default_rng(self.seed + int(idx))
            obs_indices = obs_indices.copy()
            rng.shuffle(obs_indices)
        return obs_indices

    def _extract_obs(self, data: Dict[str, np.ndarray], idx: int):
        obs_indices = self._sample_obs_indices(idx)
        obs_dict = dict()

        rgb_keys = list(self.base_dataset.rgb_keys)
        lowdim_keys = list(self.base_dataset.lowdim_keys)
        if self.base_dataset.use_embed_if_present:
            rgb_keys = []
            lowdim_keys = ["embedding"]

        for key in rgb_keys:
            selected = data[key][obs_indices]
            chw = np.moveaxis(selected, -1, 1)
            obs_dict[key] = (
                self.base_dataset.image_transforms(torch.from_numpy(chw).type(torch.uint8))
                .type(torch.float32)
                .div(255.0)
                .numpy()
            )

        for key in lowdim_keys:
            obs_dict[key] = data[key][obs_indices].astype(np.float32)

        return obs_dict

    def __getitem__(self, idx: int):
        data = self.base_dataset.sampler.sample_sequence(idx)
        obs_dict = self._extract_obs(data, idx)

        action = data["action"].astype(np.float32)
        past_start = self.anchor - self.past_action_horizon
        past_end = self.anchor
        future_start = self.anchor
        future_end = self.anchor + self.future_action_horizon

        result = {
            "obs": dict_apply(obs_dict, torch.from_numpy),
            "act_past": torch.from_numpy(action[past_start:past_end]),
            "act_future": torch.from_numpy(action[future_start:future_end]),
        }
        return result
