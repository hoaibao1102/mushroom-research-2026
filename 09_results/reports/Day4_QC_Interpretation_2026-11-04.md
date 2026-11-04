# Day 4 dataset-QC interpretation — evidence limits

The submitted Day 4 QC report uses `VERIFIED_GOOD` for two annotations and says it resolves all five train/test pairs. The submitted tables do not support a complete clearance:

1. **Different pairs audited.** The original Day 3 dHash-equal candidate pairs were: `004078↔001896`, `004072↔002583`, `004134↔000486`, `004211↔002085`, and `004252↔000323` (test ↔ train). The Day 4 file instead checked: `004012↔000105`, `004115↔000210`, `004230↔000350`, `004345↔000500`, `004450↔000720`.
2. **One image missing.** The test SHA-256 for `004012.png` is `FILE_NOT_FOUND`, not evidence of difference.
3. **Exact hashes cannot exclude near-duplicates.** The available different SHA-256 values for other submitted pairs rule out byte-identical files only; no scene-level independence is established. The five original candidate pairs remain unresolved.
4. **Annotation check is inconclusive.** Submitted RGB review asserts `VERIFIED_GOOD` for `004252` and `004472`, but other predicted/GT overlays suggest possible masks on background/foreground objects. It has not been conclusively resolved by independent polygon/annotation-ID inspection. Treat as *possible* label anomalies, not verified systematic defects.

**Research wording:** "Possible annotation anomalies and train/test near-duplicate scenes remain unresolved; test results are reported with this limitation." No reason to rerun models for this documentation.
