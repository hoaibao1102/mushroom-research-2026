# Running the Charisis and MushR notebooks

The notebooks are independent. Use a fresh Google Colab GPU runtime for each one.

| Notebook | Data | Task |
|---|---|---|
| [Charisis](Charisis_Oyster_Cluster_Growth_Tracking.ipynb) | [Zenodo 15041243](https://zenodo.org/records/15041243) | Oyster-cluster segmentation and time-lapse tracking |
| [MushR](MushR_Oyster_Maturity_Instance_Segmentation.ipynb) | [GitHub annotations](https://github.com/ETCE-LAB/mushr-mask-r-cnn) and [Kaggle images](https://www.kaggle.com/datasets/etcelab/mushr-project-raw-image-dataset-oyster-mushrooms) | Maturity segmentation and spatial flush grouping |

## Run order

1. Open the assigned notebook in Colab and select a GPU runtime.
2. Leave `RUN_MODE = 'smoke'` and run every cell from top to bottom.
3. Check that the data manifest is populated, all annotation image paths resolve, training completes, the checkpoint reloads and test inference/exports run.
4. Send the executed notebook and outputs to the team. Switch to `full` only after the smoke run succeeds.

MushR requires Kaggle credentials. Add `KAGGLE_USERNAME` and `KAGGLE_KEY` in Colab Secrets; do not put them in notebook cells or send them with the results.

## Run files

Each notebook writes a `results/` directory and a `model_bundle.zip`.

**Charisis expected results:** `run_manifest.json`, `zenodo_file_manifest.csv`, `resolved_image_manifest.csv`, training history, `test_detections.csv`, `cluster_tracks.csv`, `cluster_track_summary.csv` and `predicted_track_masks/`.

**MushR expected results:** `run_manifest.json`, train/test image manifests, `training_session_summary.json`, `mushr_instance_predictions.csv`, `mushr_flush_predictions.csv` and `predicted_masks/`.

Full mode also writes COCO mask metrics. Those metrics are not expected in smoke mode.

## What to send back

- The executed `.ipynb` with outputs retained.
- The notebook's `results/` folder and `model_bundle.zip`.
- `run_note.txt` with pass/fail, GPU, Python/PyTorch/TorchVision versions, run mode and any settings changed.

If a run fails, send the executed notebook and a `failure.txt` with the first failing cell and full traceback. Do not send raw dataset archives or credentials. Do not change model architecture, labels or splits while troubleshooting; note any required change for team review.

## Notes

The notebooks use TorchVision adaptations of the papers' Mask R-CNN model families, not exact MMDetection/Detectron2 reproductions. Charisis labels (`immature`, `well-defined`, `overstayed`) and MushR labels (`not-ready`, `ready`, `overdue`) are different and must stay separate. Smoke runs test the pipeline, not model quality. Real dataset downloads and Colab GPU runs have not yet been verified.
