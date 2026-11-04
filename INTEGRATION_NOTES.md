# Integration notes — repository update through Day 3 (2026-11-03)

This is a **repository file bundle**, not a Git commit or push. It was created from the previously supplied **30 October 2026 Team 10 repository snapshot** and the uploaded Day 2/Day 3 evidence. The user's latest displayed file tree includes `file_list.txt` whereas the earlier snapshot did not; a new file list is generated here. **If your live clone was edited after that snapshot, compare diffs and do not blindly replace those newer changes.** A fresh repo ZIP would enable a truly exact in-place merge.

## Files added

- Day 2 two-class and WB-only test metric JSON, configs, reports and user-supplied console-log excerpts.
- Day 3 Thịnh area source scripts, source QC and the 30-image area-evaluation CSV/JSON/Markdown; Khang original plus corrected 12-image error-analysis CSV/Markdown.
- 16 original uploaded figures, curated in `10_research_paper/figures/` (12 prediction + 4 area), current Markdown and Word research-paper drafts.
- Three Colab notebooks under `08_experiments/notebooks` with explicit execution/provenance warnings; no raw data or model weights.
- Experiment registry, status/decision log, Git-friendly navigation and reproducibility manifest.

## Existing files updated

`README.md`, `START_HERE.md`, `00_project_management/{RESEARCH_STATUS.md,TASK_BOARD.md,DECISION_LOG.md,project_state.json}`, `08_experiments/{README.md,experiment_registry.csv}`, `09_results/README.md`, `12_reproducibility/CLOUD_EXECUTION_GUIDE.md`, the workspace validator/tests, the C03 QC issue log, and provisional selected research notes.

## Important science and administration caveats

- **Day 1 EDA → Day 2 approach reproduction → Day 3 further analysis.** The earlier named `M18K_Day2_Reviewed_Evidence_2026-11-03.zip` contained **Day 3** evidence, relabeled correctly in this repo.
- Day 2 reproduces the YOLOv8 method **on V2**, not the original paper's exact benchmark or numerically comparable AP.
- The original WB training notebook includes an incorrect two-class test cell; only the corrected separate held-out WB test is cited.
- Thịnh's 207.4 px² area MAE / 8.80% mean relative error apply **only to 4,900 matched masks on 30 images**, not the full test set or physical mm².
- Five perceptual dHash matches and two suspicious GT overlay cases remain **unverified**.
- Formal dataset/license selection and QC gates remain open; model performance does not imply regulatory/data-permission approval.

## Merge and checks

1. Back up / commit the current live clone; **keep its `.git` directory**.
2. Extract/merge this archive, review `git status` and `git diff`, and inspect changed canonical docs and new figures for redistribution rights before pushing.
3. Run `python scripts/validate_workspace.py`, `python -m unittest discover -s tests -v`.
4. Ensure Git does not include raw data, source COCO JSON, big WB-label ZIP, checkpoints or credentials.

The source snapshot's historical `setup_reports/` and candidate C01/C02 are preserved untouched.

## Day 4 merge patch (2026-11-04)

The Day 4 patch ZIP preserves the `mushroom-research-2026/` root and contains **only newly added or modified files relative to the Day 3 repository snapshot**. Extract into the **parent directory of the repository**, or copy the contents of its `mushroom-research-2026/` directory into your clone after reviewing differences. Existing Day 1–3 files not modified by this patch are not included.

- `README.md`, `START_HERE.md`, project state/board, results indexes, experiment registry, `.gitignore`, tests and validator have been updated for Day 4.
- New executed Colab notebooks are under `08_experiments/notebooks/`; area/QC source under `07_source_code/evaluation/`; all new metrics and evidence under `09_results/`; English IVP course draft under `10_research_paper/drafts/`.
- Selected small PNGs and the compressed matched-mask CSV have explicit `.gitignore` exceptions. Raw dataset, checkpoints and output ZIP archives stay excluded.
- Source ZIP hashes are recorded in `12_reproducibility/manifests/DAY4_EVIDENCE_2026-11-04.json`.
- Run `python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v`; neither means the original dataset has been freshly audited.

The source repository snapshot was the previously delivered **Day 3 full repository ZIP**; if there are newer uncommitted local changes, merge selectively rather than blindly overwriting them.
