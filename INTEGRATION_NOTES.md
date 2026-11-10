# Integration notes

This repository is the research record for Mushroom Research 2026. It keeps source and dataset reviews, experiment definitions, evaluation results, reproducibility notes and field-validation plans. The Day 8 application folder is a prototype snapshot for traceability; ongoing product development is intended to live in a separate application repository.

## System boundary

- **Training:** Google Colab GPU; export versioned model bundles.
- **Local application:** load an exported bundle and run image inference, tracking, measurements, storage and review without a live Colab session.
- **Runtime target:** AMD acceleration is the priority to test, with CPU inference as the required fallback. Hardware acceleration is not considered supported until the actual target machine completes an inference run.
- **Data scope:** Charisis and MushR are oyster-mushroom sources with different labels and tasks. M18K V2 remains historical white-button evidence, not the selected general production dataset.

## Source roles

- **Charisis:** temporal oyster-cluster segmentation and tracking reference.
- **MushR:** oyster fruitbody maturity segmentation and within-image spatial grouping reference.
- **M18K V2:** prior YOLOv8n-seg baseline, area analysis and Gradio demo evidence.

Do not merge source taxonomies or compare their metrics as if they came from one dataset. Keep the D001 exclusion enforced.

## Day 8 application handoff

The prototype snapshot is in [`13_local_application/`](13_local_application/README.md). Its seven unit tests pass. The uploaded source archive has model-registry metadata but no trained checkpoint, so it does not establish real-checkpoint inference quality. DirectML/AMD acceleration, camera calibration for mm² measurements, multi-species model quality and field performance remain open.

Add the external application repository URL to the root README when the destination repository is available. Keep active application issues and implementation changes there; use this repository for research decisions and evidence.
