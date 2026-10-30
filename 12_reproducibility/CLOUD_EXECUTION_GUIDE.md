# Colab / Google Drive execution guide — M18K

## Current data workflow

The executed notebook uses `MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/`, containing `train`, `valid`, `test`; each split supplies an annotation JSON and `rgb/` and `depth/` directories. Data remain on Drive; do not redownload on each runtime session. The notebook streamed large JSON (~2 GB train annotations) to avoid RAM exhaustion. Python 3.13.18 was printed in its saved output; record the full package versions before a model experiment.

## Training tomorrow (not done today)

Use a GPU Colab runtime if available; GPU assignment is not guaranteed. For performance, consider a temporary **local Colab cache** copied from Drive when space allows, while preserving immutable Drive source files. Save model checkpoints and run logs persistently to Drive. Keep fixed seeds and metadata in `08_experiments/`, and do not modify test split during model selection.

## Required records for a real run

Record notebook/Git commit, Python/CUDA/PyTorch/Ultralytics versions, hardware, data release and hashes, train/val/test manifests, model/configuration, random seeds, actual start/end timestamps, validation-selected checkpoint and final unseen-test per-class metrics. Do not claim results until output evidence exists.
