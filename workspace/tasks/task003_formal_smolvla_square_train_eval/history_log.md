# History Log

<!-- METADATA:SESSION=0 -->

## Session 0
- Created task for formal SmolVLA-style square training and 100-epoch interval evaluation.
- Implemented `scripts/train_eval_smolvla_square_formal.py` for isolated epoch-based training/eval.
- Copied the square HDF5 dataset into the intern-owned task storage path before training.
- Started a 2-GPU H200 DDP run for 1000 epochs with evaluation every 100 epochs.
- Reached epoch 100 and saved `epoch_0100.pt`; offline square action eval recorded `val_loss=0.20909729599952698` and `val_sample_action_mse=0.13123467564582825`.
- Completed 1000 epochs and saved checkpoints `epoch_0100.pt` through `epoch_1000.pt`.
- Final epoch 1000 offline square action eval: `val_loss=0.3399428427219391`, `val_sample_action_mse=0.13218089938163757`.
- Best sampled action MSE was epoch 300: `0.13077014684677124`.
- Wrote final report to `/mnt/3fs2/data/tingwen.du/intern_method_developer/task003_formal_smolvla_square_train_eval/reports/REPORT.md`.
