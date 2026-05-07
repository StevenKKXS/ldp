#!/usr/bin/env python3
"""Generate the robomimic BC-RNN image config used for issue #157 checks."""

import argparse
import json

from robomimic.config import config_factory
from robomimic.scripts.generate_paper_configs import (
    modify_bc_rnn_config_for_dataset,
    modify_config_for_dataset,
    modify_config_for_default_image_exp,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--config-out", required=True)
    parser.add_argument("--name", default="core_bc_rnn_square_ph_image_v141_issue157")
    parser.add_argument("--num-epochs", type=int, default=600)
    parser.add_argument("--rollout-n", type=int, default=50)
    parser.add_argument("--rollout-horizon", type=int, default=400)
    parser.add_argument("--rollout-rate", type=int, default=20)
    parser.add_argument("--save-every", type=int, default=20)
    parser.add_argument("--epoch-steps", type=int, default=500)
    parser.add_argument("--valid-steps", type=int, default=50)
    parser.add_argument("--seed", type=int, default=1)
    args = parser.parse_args()

    config = config_factory("bc")
    modify_config_for_default_image_exp(config)
    modify_config_for_dataset(
        config=config,
        task_name="square",
        dataset_type="ph",
        hdf5_type="image",
        base_dataset_dir="/unused",
    )
    modify_bc_rnn_config_for_dataset(
        config=config,
        task_name="square",
        dataset_type="ph",
        hdf5_type="image",
    )

    with config.values_unlocked():
        config.experiment.name = args.name
        config.experiment.epoch_every_n_steps = args.epoch_steps
        config.experiment.validation_epoch_every_n_steps = args.valid_steps
        config.experiment.save.every_n_epochs = args.save_every
        config.experiment.rollout.n = args.rollout_n
        config.experiment.rollout.horizon = args.rollout_horizon
        config.experiment.rollout.rate = args.rollout_rate
        config.experiment.render_video = True
        config.experiment.keep_all_videos = False
        config.train.data = args.dataset
        config.train.output_dir = args.output_dir
        config.train.num_epochs = args.num_epochs
        config.train.seed = args.seed

    with open(args.config_out, "w", encoding="utf-8") as f:
        json.dump(json.loads(str(config)), f, indent=4)
        f.write("\n")
    print(args.config_out)


if __name__ == "__main__":
    main()
