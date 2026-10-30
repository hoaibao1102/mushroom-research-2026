# WP-05 — Research Candidate Decision & Fallback Screening

**Date:** 2026-10-30

**Branch:** `research/wp-05-candidate-decision`

**Dataset selected:** `NO`

**Training authorized:** `NO`

**Research gap validated:** `NO`

## Checkpoint status

WP-04C was committed and pushed successfully:

- Commit: `69215062f29d0d9bfe3ce194eafb4001097d8138`
- Message: `docs(research): complete WP-04C final provenance decision`
- Remote branch: `origin/research/wp-04c-final-decision`
- Remote SHA read-back matched local SHA.
- No force-push or merge occurred.

## C03 follow-up

The author inquiry remains `DRAFT_NOT_SENT`. The corresponding-author contact is verified from saved primary XML. A human sending/tracking checklist was created. C03 remains `CONDITIONAL_GO` only for clarification and `NO_GO_FOR_PRIMARY_GENERALIZATION` under current evidence.

## Bounded fallback scope

Exactly three existing WP-03 candidates were screened; no new candidate search and no dataset download occurred:

- C04: shiitake phenotype detection — `HOLD`
- C05: white-button RGB-D time series — `CONDITIONAL_GO` for bounded verification, `HOLD` for selection
- C08: M18K detection/pose/growth — `HOLD`

## Decision

No candidate is ready for selection or training. C05 is the best next bounded verification direction because identity, license, paper relation, and native temporal task are comparatively clear. It is not yet a defensible independent-generalization benchmark: repeated observations from two beds, unresolved 129/128/12 manifests, absent grouped split, and missing runnable method code remain blockers.

C04 has stronger shiitake cultivation adjacency but high lineage/protocol effort. C08 is blocked first by dataset asset-license uncertainty, then by version/count/grouping conflicts.

## Recommended action

Before 2026-11-06:

1. Manually send and track the C03 inquiry if approved.
2. Request explicit authorization only for a bounded C05 payload/grouping preflight; do not train.
3. Define acceptance and rejection gates before acquiring data.
4. On the deadline, compare actual C03 evidence with the bounded C05 preflight. If neither supports a defensible estimand, stop and revise the research direction rather than forcing a winner.

## Evidence boundary

All fallback findings come from existing WP-03/WP-04 saved primary evidence and audit reports. Source-reported counts, IDs, metrics, and splits are not treated as independently reproduced facts. Unknowns remain `UNVERIFIED`; no numerical scoring was applied.
