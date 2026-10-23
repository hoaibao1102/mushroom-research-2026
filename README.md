# Mushroom Research 2026

University Software Engineering capstone: mushroom cultivation research with possible computer vision / machine learning. This is a fresh research workspace, not a continuation of DS-02.

## Objectives
1. Validate a meaningful cultivation problem, including whether AI is necessary.
2. Establish public dataset provenance and review relevant papers.
3. Reproduce a suitable published baseline, only after authorization.
4. Investigate an evidence-backed gap and conduct controlled experiments.
5. Write a research paper; assess future feasibility at a small oyster mushroom farm if justified.

## Current phase and research status
**PHASE 0 — DATASET & RESEARCH TOPIC SELECTION**, WP-00 infrastructure only.
No dataset, paper, confirmed gap, baseline, training authorization or external validation.
Canonical status: `00_project_management/project_state.json`; human-readable mirror: `RESEARCH_STATUS.md` in the same directory. Update both through a reviewed decision.

## Candidate datasets — all PENDING_VERIFICATION
- C01: substrate contamination classification; https://data.mendeley.com/datasets/jrbx34k77g/2 . A paper using this exact dataset has NOT been confirmed.
- C02: harvest readiness; https://www.kaggle.com/datasets/etcelab/mushr-annotated-dataset-oyster-mushrooms . Possible associated paper to verify: https://www.mdpi.com/2077-0472/13/8/1533 . Dataset-paper relationship is NOT_VERIFIED.
- Another candidate may be added later using a new unique ID; selection is not limited to these two.

Excluded: Annotated Oyster Mushroom Images, identifier `hf55tkx489` (abandoned DS-02). No other dataset is excluded. C02 identity/possible overlap remains unknown and must be checked, not presumed.

## Research methodology
Domain evidence → source verification → QC and grouped leakage-safe splits → reviewed selection → baseline reproduction → falsifiable gap → controlled paired experiments → conclusions/limitations → external readiness. Prefer suitable 2024–2026 papers while retaining earlier foundational work. No unsupported custom losses or automatic algorithm selection.
Every claim must be tagged VERIFIED_FACT, SOURCE_CLAIM, PRACTITIONER_OBSERVATION, HYPOTHESIS or UNKNOWN, with source/evidence location, date and reviewer. A linked URL is not verification.

## Directory overview
| Directory | Responsibility |
|---|---|
| 00_project_management | Charter, status, decisions, tasks, meetings, milestones |
| 01_domain_research | Cultivation workflows, terminology, observed pain points |
| 02_literature_review | Paper registry, summaries, comparisons, gap evidence |
| 03_dataset_discovery | Candidate/exclusion registries, screening and provenance |
| 04_dataset_candidates | Independent candidate metadata, raw data, QC and reports |
| 05_research_protocols | Screening, integrity, leakage, reproducibility and gates |
| 06_selected_research | Selection decision reference only; currently unselected |
| 07_source_code | Future data/features/models/training/evaluation utilities |
| 08_experiments | Future configs, ignored runs/checkpoints, experiment registry |
| 09_results | Metrics, visualizations, statistics, error analysis, reports |
| 10_research_paper | Outline, drafts, figures, tables, references, submission |
| 11_field_validation | Future protocols, isolated ignored external images, reports |
| 12_reproducibility | Environments, manifests, snapshots and cloud guidance |
| scripts / tests / setup_reports | Standard-library validators, tests and setup evidence |

## Setup
Read `START_HERE.md`. Python 3.11+ recommended (3.11/3.12 for later ML compatibility checks); WP-00 standard-library utilities are tested with the interpreter recorded in the setup report. No dependencies need installation.
```sh
python scripts/validate_workspace.py
python scripts/show_project_status.py
python -m unittest discover -s tests -v
```
Validator is deliberately a **WP-00 clean-initialization validator**, not a future downloaded-dataset QC program. Extend it through a reviewed later work package, not by suppressing failures.

## Next work packages
WP-01: Candidate Dataset & Paper Source Verification only; human-reviewed scope before any downloads. Later packages for QC, selection, baseline and experiments must be separately specified/authorized. WP-00 does not advance to WP-01.
