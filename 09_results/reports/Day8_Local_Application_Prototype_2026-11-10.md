# Day 8 — local application prototype (10 November 2026)

Today the first local Mushroom Growth Monitor prototype was assembled from the Day 6 system design. The research repo now keeps a snapshot of that implementation for reference; ongoing application development is intended to live in a separate repository.

## Application prototype

The Streamlit app in [`13_local_application/`](../../13_local_application/) connects the main workflow:

- cultivation sites, growing units and cameras;
- image import, capture metadata and SHA-256 de-duplication;
- model-bundle import and version activation;
- instance-segmentation inference, cluster tracking and pixel-area measurements;
- MushR per-image flush grouping, environmental CSV records and human review;
- COCO export of reviewed samples for later training.

The Charisis and MushR paths remain separate. Charisis predictions are used for temporal cluster tracking; MushR fruitbodies are grouped spatially within each image. A MushR flush ID is not a persistent track. Area remains in px² unless a camera-specific calibration is available.

## Checks and limits

- The application unit suite passed **7/7** tests. Coverage includes database operations, image de-duplication, bundle metadata/import, maturity grouping and multi-frame tracking.
- `tools/system_check.py` ran successfully in the packaged source environment. It found one active MushR registry entry, but **no checkpoint file**; no captures were present. The current archive therefore does not establish real-checkpoint inference quality.
- The check environment used CPU-only PyTorch. DirectML was unavailable there, and the target Windows/RX 5500 XT acceleration path remains unverified.
- The available model families are oyster-mushroom-specific. The application structure is broader, but multi-species model performance has not been demonstrated.
- The app's software tests do not validate the Streamlit workflow end to end, trained model accuracy, physical-size calibration or field performance.

The user has confirmed that the local prototype is working overall. The checks above are the validation that can be reproduced from this repository snapshot; they should not be read as a model benchmark.

## Repository split

This repository remains the research record: source reviews, dataset audits, experiments, metrics, reproducibility and validation evidence. The `13_local_application/` folder is retained as the Day 8 prototype snapshot, not as the ongoing application development location. The separate application repository URL has not yet been added to the project README.

## Next work

1. Put the application source of truth in its separate repository and add that URL to the research README.
2. Keep model-quality claims tied to executed, reproducible evaluations on the relevant held-out data.
3. Validate the real model bundles and end-to-end image workflow on the target Windows machine.
4. Test the AMD path separately; retain CPU inference as the fallback until GPU execution is demonstrated.
5. Continue research-side dataset/schema checks, calibration and external/field validation.
