# Integration notes for the team repository

This deliverable is **an edited repository tree without `.git`**, not a push or commit. To preserve Git history, merge these files into your existing clone, review `git diff`, then commit/push through your normal team workflow. Nothing has been uploaded to your GitHub account.

## Changes

- Preserved the common `00`–`12` organization, legacy C01/C02 candidate records and historical setup evidence.
- Added **C03 M18K V2** as a *working candidate*, recorded the actual completed 30 Oct notebook, curated EDA tables/figures, and a results report.
- Updated README, project management, source, literature, QC, experiments and reproducibility records to the M18K direction.
- Replaced the obsolete clean-only WP-00 validator with a structure/evidence consistency validator plus tests, without claiming full dataset QC.
- Did **not** include raw V2 data, depth arrays, 2.5-GB annotation JSON, model weights, or confidential Drive credentials.

## Human review required

1. Decide whether C03 is officially selected and update `DECISION_LOG.md`, `project_state.json` and `06_selected_research` with reviewer/date.
2. Review upstream V2 reuse/license terms and record archive hash, version and download method.
3. Independently audit rare BB annotations and scene/near-duplicate leakage; resolve count discrepancy.
4. Review notebook figures before public posting if the upstream dataset prohibits redistribution.
5. Do not enter benchmark accuracy until training and held-out evaluation actually complete.

## Checks performed on this edited tree

`python scripts/validate_workspace.py` and `python -m unittest discover -s tests -v`. The validator checks metadata consistency and prohibited payloads; it cannot confirm the original Google Drive data.
