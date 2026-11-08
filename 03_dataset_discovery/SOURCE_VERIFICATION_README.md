# Source verification records

Use `SOURCE_DATA_AUDIT_DAY6.md` for the source-role summary and `SOURCE_CODE_REGISTRY.csv` for repository contents/licensing notes. Use `candidate_registry/CANDIDATE_REGISTRY.csv` for dataset-level access, task fit, verification and QC status.

## Increment 1 retrieval order

1. **Charisis / Zenodo 15041243:** inspect record metadata and a small archive sample first; preserve experiment, sequence and timestamp fields.
2. **MushR / ETCE-LAB:** retrieve the Mask R-CNN code and COCO annotation JSONs before acquiring matching raw images; inspect release assets and check data licence separately from code licence.
3. **M18K:** inspect the distinct growth-monitoring subset as optional supporting material; keep its prior V2 experiments domain-scoped.
4. **Optional six-species collection:** consider only for species-breadth image classification/robustness, not temporal tracking.

For every retrieved asset, record the exact URL/release, retrieval date, filename, SHA-256, archive size, licence and extraction result. A public paper/repository page does not prove that an archive, checkpoint or annotation file has been downloaded and run locally.

The user does not need to upload public source code or dataset archives. Any required Kaggle credential must be entered privately in the user's own Colab Secrets.
