# Reproducibility protocol v1

WP-00 uses standard library only. Future execution must retain:

- Environment: OS/architecture, Python executable/version, CPU/GPU/driver/CUDA where applicable, dependency lock/export, creation commands and UTC/offset timestamps in `12_reproducibility/`.
- Seeds: explicit Python/library/framework/data-loader seeds and deterministic flags; state nondeterministic operations. Use a preregistered paired seed list rather than selecting favorable seeds.
- Data: exact source/version/license, original and extracted SHA-256 manifests, QC code/version and transformations. Never version bulk data or DS-02 artifacts.
- Splits: immutable relative-path/hash/label/group/split manifests, grouping rationale, independent-unit definition and version/hash. Shared identical splits across comparisons.
- Experiment IDs: `EXP-YYYYMMDD-NNN` allocated only on actual approved execution; registry links protocol, config, environment, dataset/split, seeds, code Git commit and dirty diff if unavoidable. WP-00 registry stays headers only.
- Models/dependencies: architecture/package versions, initialization source/license/hash, optimizer/scheduler, preprocessing, hyperparameters and resource budget.
- Checkpoints: ignored local storage; record location, hash, epoch/step, selection rule and provenance in manifests. No weights downloaded in WP-00.
- Metrics: preserve raw predictions where legally permitted, metric definitions/code, per-class/group results, uncertainty estimates, statistical assumptions and complete negative/null outcomes. Never fabricate missing results.
- Git: code commit reference for every future run; record uncommitted patch hash if necessary and explain. WP-00 creates no commit.
- Reproduction: independent rerun from documented environment/config/manifests; predeclare tolerance, compare outputs and explain differences. Keep test set sealed until final evaluation.

Evidence record: statement, evidence tag, exact source/section or artifact path/hash, date, reviewer, scope and counterevidence. Provenance is required for source claims as well as verified facts.
