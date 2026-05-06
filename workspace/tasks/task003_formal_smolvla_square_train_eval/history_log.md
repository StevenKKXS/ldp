# History Log

<!-- METADATA:SESSION=0 -->

## Session 0
- Created task for formal SmolVLA-style square training and 100-epoch interval evaluation.
- Implemented `scripts/train_eval_smolvla_square_formal.py` for isolated epoch-based training/eval.
- Copied the square HDF5 dataset into the intern-owned task storage path before training.
- Started a 2-GPU H200 DDP run for 1000 epochs with evaluation every 100 epochs.
- Reached epoch 100 and saved `epoch_0100.pt`; offline square action eval recorded `val_loss=0.20909729599952698` and `val_sample_action_mse=0.13123467564582825`.
