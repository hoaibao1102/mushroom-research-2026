# Start here

1. Enter the workspace (PowerShell):
   ```powershell
   Set-Location 'D:\Capstone\mushroom-research-2026'
   ```
   Git Bash alternative: `cd /d/Capstone/mushroom-research-2026`.
2. Check Git: `git rev-parse --show-toplevel` and `git status --short --branch`. Expected root is this folder. If no repository exists and no ancestor owns it, use `git init --initial-branch=main`. Do not initialize within an unrelated ancestor repository; do not commit secrets, data or historical artifacts. WP-00 creates no commits.
3. Recommend Python 3.11/3.12 for later ML ecosystem support, subject to baseline requirements. WP-00 needs only Python 3.11+ standard library; check `python --version`. No venv or package install is required for these utilities. Optional future venv: `python -m venv .venv`.
4. Run `python scripts/validate_workspace.py`, `python scripts/show_project_status.py`, and `python -m unittest discover -s tests -v`. A nonzero validator exit must be investigated.
5. **Do not download in WP-00.** Once separately authorized, put original candidate payloads under `04_dataset_candidates/<candidate>/raw/`, never in code or Git. Store provenance/license/version/download timestamp/SHA-256 manifests in that candidate's `source/` and `dataset_metadata/`. Keep raw immutable; declare processed/derived data separately under candidate `processed/` (ignored) and preserve transformation scripts/manifests. Future farm images belong only under `11_field_validation/external_test_data/` and remain isolated from model selection.
6. Prepare WP-01 using `03_dataset_discovery/candidate_registry/CANDIDATE_REGISTRY.csv`, the exclusion registry, and `05_research_protocols/DATASET_SCREENING_PROTOCOL.md`. Verify exact identity and versions, legal access/license, paper relationship and the DS-02 overlap question before proposing any download. No website verification was performed by WP-00.
7. Before reviewed dataset selection: do not train, download weights, implement a detector, tune against test data, claim a gap, fabricate statistics or reuse DS-02 artifacts. Baseline training requires G0/G1 GO, recorded selection, frozen protocol and explicit training authorization; G2 is the outcome of authorized baseline reproduction, not a prerequisite for baseline training.

Evidence tags: VERIFIED_FACT (independently checked), SOURCE_CLAIM (attributed only), PRACTITIONER_OBSERVATION (dated contextual testimony), HYPOTHESIS (testable expectation), UNKNOWN (not established). Use `12_reproducibility/manifests/EVIDENCE_TEMPLATE.md`.
