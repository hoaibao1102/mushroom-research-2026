# Experiment protocol template — no execution authorized

## Entry and authorization
Baseline reproduction: G0/G1 GO, reviewed dataset selection, frozen protocol/splits, resource budget and explicit training authorization. G2 is assessed after reproduction. Improvements additionally require G2/G3 GO and a preregistered testable hypothesis. No experiment IDs/results are populated in WP-00.

## Pre-execution record
- Problem, independent sampling unit, non-ML comparator and falsifiable hypothesis.
- Source baseline/code/license and exact versions; reproduction acceptance tolerance defined before runs.
- Primary metric and practical improvement threshold justified by cultivation use; secondary metrics/guardrails, failure costs and resource budget.
- Frozen train/validation/test manifests; test access policy, group definitions and leakage audit.
- Fixed paired seed list, equal tuning/compute budget, one controlled change per ablation, stopping rules and exclusions.
- Analysis plan: aggregate at independent-unit level; appropriate paired tests/cluster bootstrap, confidence intervals/effect sizes and multiple-comparison control where applicable. Justify precision/power; do not assert iid images when batches are correlated.
- Protocol/config/environment/commit links, owner and explicit approval.

## Execution and reporting (future)
Allocate real ID, log all seeds/runs/resources/failures; select checkpoints only on validation. Preserve metrics/predictions/checkpoint hashes. Report all outcomes, uncertainty and deviations; no cherry-picking or repeated test peeking. Assess practical benefit, not significance alone. Independently review claims and limits before gate decisions. Negative/null results are valid scientific findings. No required accuracy gain or fabricated statistical guarantees.
