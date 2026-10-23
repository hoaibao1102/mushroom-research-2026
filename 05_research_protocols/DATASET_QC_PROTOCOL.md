# Dataset QC protocol v1 — execution deferred

Entry: G0 GO, confirmed legal access and explicit download/QC authorization. WP-00 contains no data and performs no dataset QC.

1. Record source/version/license/download time and SHA-256 of original archives and every extracted file; retain immutable originals. Document extraction tool and relative paths; never execute dataset-supplied code without review.
2. Enumerate sizes/types, decode integrity, dimensions/channels/orientation and unsupported formats. Record corrupt/missing/truncated files and any quarantine/removal decision; never silently drop files.
3. Validate label schemas/class vocabulary, missing/unknown labels, classification folder mappings, detection box bounds/coordinates, class IDs and image-annotation pairing as applicable. Sample manually using a declared stratified audit plan; preserve disagreements and adjudication evidence.
4. Audit metadata: specimen/bag/batch/farm/session/frame/time IDs, acquisition conditions and privacy. Mark missing group information as unresolved, not independent samples.
5. Compute exact hashes; use a justified near-duplicate approach with threshold calibration and manual review. Group derived crops/augmentations and same original frames. Summarize per-group and per-class counts only from real measured data.
6. Partition independent groups, not individual images; respect batch, biological-unit and temporal boundaries. Fit preprocessing on train only; augment train only. Keep external tests separate. Freeze manifests with hash, group ID, label, source version and split; review DATA_LEAKAGE_CHECKLIST.md.
7. Assess class imbalance, outliers, sampling bias and test uncertainty at the independent-unit level. Document metric feasibility without fabricating a minimum sample count. No test-driven tuning.
8. Produce reproducible QC report with commands/code version, manifests, exclusion decisions, residual leakage risks and reviewer. G1 requires explained integrity/label issues and defensible splits; unknown critical groups block GO.

Outputs: metadata/schema, checksums, label and group audit tables, duplicate-group manifest, split proposal/frozen manifests, QC report and decision. Derived data must be separately stored in ignored candidate `processed/`; transformations and manifests are versioned.
