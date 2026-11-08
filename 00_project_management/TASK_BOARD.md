# Task board — Day 6 (8 November 2026)

| Work package | Status | Evidence / exit condition |
|---|---|---|
| Days 1–5 — M18K V2 experiments | Preserved as completed historical evidence | Original notebooks, metrics and reports retained; results remain limited to the recorded M18K / WB domain |
| WP-06 / Increment 0 — target requirements | Done | `PROJECT_CHARTER.md`, `SYSTEM_REQUIREMENTS.md`, `TARGET_SYSTEM_REQUIREMENTS.md` |
| WP-06 / Increment 0 — public source audit | Done | `SOURCE_DATA_AUDIT_DAY6.md`, paper/dataset/source-code registries and candidate notes |
| WP-06 / Increment 0 — architecture and update lifecycle | Done | `SYSTEM_ARCHITECTURE.md`; Colab training/local inference split; reviewed-data promotion policy |
| WP-06 / Increment 0 — repository validation | Done | `scripts/validate_workspace.py` and `tests/` |
| WP-07 / Increment 1 — retrieve data samples | Next | Retrieve Charisis Zenodo metadata/sample and MushR annotations; log versions, licences and SHA-256 hashes |
| WP-07 / Increment 1 — dataset adapters | Not started | COCO/source adapters preserve source classes, image identity, camera/sequence IDs and timestamps |
| WP-07 / Increment 1 — visual/schema QC | Not started | Verify real images, masks, missing references, dimensions, categories and split/group fields |
| WP-07 / Increment 1 — unified manifest | Not started | Validate image ID, timestamp, camera, grow-unit and batch associations |
| WP-08 / Increment 2 — model prototype | Blocked on Increment 1 | Select YOLO-seg or Mask R-CNN route using actual annotations and export/runtime compatibility |
| WP-09 / Increment 3 — tracking/growth | Planned | Persistent grow-unit-scoped IDs, track events, growth measurements and multi-date tests |
| WP-10 / Increment 4 — local runtime | Planned | CPU fallback and AMD execution tested on target desktop; report actual provider and memory |
| WP-11 / Increment 5 — local application | Planned | Local storage, inference API, dashboard and export workflows |
| WP-12 / Increment 6 — integration/field tests | Planned | Full offline workflow and target-scene validation |

## Advancement rules

- Do not train before the selected data adapters load and visualize real samples correctly.
- Keep each dataset's class map and annotation semantics traceable.
- Split by independent experiment/sequence/batch wherever possible; prevent adjacent-frame leakage.
- Do not convert px or depth values to physical units without calibration/reference evidence.
- Do not accept unreviewed pseudo-labels as ground truth.
- Do not promote a candidate model without fixed regression evaluation.
- Preserve the deployed checkpoint for rollback.
