# WP-05 Recommendation

## Decision

**No candidate receives unconditional `GO`. No final dataset or topic is selected.**

### C03

- `CONDITIONAL_GO` for author clarification only.
- `NO_GO_FOR_PRIMARY_GENERALIZATION` under current evidence.
- Manual review date: 2026-11-06.

### Fallbacks

1. **C05 — `CONDITIONAL_GO` for bounded payload/grouping verification only; `HOLD` for selection.**
2. **C04 — `HOLD`.**
3. **C08 — `HOLD`; dataset asset license is a hard unresolved gate.**

## Best next research direction

Prioritize a narrow C05 feasibility preflight for **same-facility RGB-D cap segmentation/tracking under explicit temporal and parent dependence**. This is a verification direction, not a selected thesis topic. It is preferable to another broad discovery round because C05 already has:

- exact dataset and paper identities;
- CC BY 4.0 metadata;
- explicit RGB-D/COCO structure;
- reported temporal acquisition and baseline methods.

Before any protocol approval, verify the 129 RGB-depth pairs and COCO references, reconcile 129/128/12 subsets, recover parent/time grouping, and determine whether enough independent support remains for a defensible estimand. If not, reject C05 rather than relax independence requirements.

## Why not C04 or C08 first?

- C04 requires a 4.11 GB payload audit, augmentation lineage reconstruction, count reconciliation, and resolution of material code/paper conflicts; it also does not transfer directly to oyster cultivation.
- C08 requires data-license verification before scientific reuse, then release/count and scene/sequence grouping reconciliation.

## Hard boundaries

- Do not train models.
- Do not download a complete dataset without explicit authorization.
- Do not create specimen IDs from image similarity.
- Do not mark a research gap validated.
- Do not interpret C03 silence as author rejection.
- Do not select a candidate automatically.

## Action before 2026-11-06

1. Human completes and manually sends the C03 inquiry, then updates the tracker with actual evidence.
2. If authorized, conduct metadata-first C05 payload planning: expected files, storage, checksums, grouping fields, and stop gates—without training.
3. At the deadline, decide whether C03 evidence closes the biological claim; otherwise retain its primary-generalization NO-GO and compare it against the verified C05 preflight.
