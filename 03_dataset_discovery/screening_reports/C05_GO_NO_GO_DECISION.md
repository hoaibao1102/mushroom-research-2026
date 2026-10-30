# C05 GO / NO-GO Decision

## Decision

**`HOLD`**

C05 does not satisfy the current rule for `GO_FOR_DEEP_QC`. Necessary files and labels are described, but exact subset membership, annotation coverage, leakage-safe evaluation membership and baseline reconstruction are not sufficiently supported by the bounded public evidence.

This is not `NO_GO_FOR_CURRENT_RESEARCH_GOAL` because the dataset-paper relationship, research-use licence, temporal acquisition and segmentation task are credible enough to remain scientifically interesting. The hold prevents premature capstone selection or training.

## Decision gates

| Gate | Result | Basis |
|---|---|---|
| Exact dataset-paper identity | PASS | Versioned Mendeley DOI and directly related method/data papers are identified. |
| Research-use licence | PASS | Mendeley metadata displays CC BY 4.0. |
| Necessary modalities described | PASS_AUTHOR_REPORTED | RGB, depth and COCO instance annotations are described. |
| Canonical file inventory | FAIL_NOT_VERIFIED | File tree/checksums were not available in the bounded metadata pass. |
| 129/128 reconciliation | FAIL | The differing scopes are known; the one-mosaic difference is unexplained. |
| 12-image benchmark identity | FAIL | No filename/member list was found. |
| COCO coverage for all 129 | FAIL_NOT_VERIFIED | No per-mosaic inventory was inspected. |
| Leakage-safe historical split | FAIL | No image/patch/parent membership manifest was found. |
| Time grouping | PARTIAL | Date/cycle ordering exists; independent grouping does not follow from it. |
| Bed grouping | FAIL_NOT_VERIFIED | Two beds are reported, but record-level bed IDs were not verified. |
| Exact YOLO reproduction | FAIL_NOT_VERIFIED | Several headline parameters exist; environment, seeds, model sizes, configs, manifests and checkpoint identity are incomplete. |
| Engineering manageability | CONDITIONAL | RGB-only work is moderate; provenance reconstruction and RGB-D tracking reproduction are high complexity. |
| Defensible narrow research question | CONDITIONAL | Temporal/dense-boundary robustness could be meaningful; architecture substitution alone is not. |

## Scientific exploration versus capstone suitability

### Scientific exploration: `CONDITIONAL_YES`

C05 can support exploratory work on RGB-D mushroom-cap segmentation, dense-scene boundary quality, temporal tracking and harvesting perception. The public record is substantially clearer than C03 on acquisition timing and annotation format and clearer than C04 on the immediate dataset-paper relationship.

Exploration must not treat temporal mosaics or cap instances as independent biological samples. Claims should remain limited to the observed facility, beds and cycle unless further independent data appear.

### Current capstone selection: `NO_NOT_YET`

A capstone benchmark needs a traceable evaluation unit and leakage-safe membership. Without the 12-image list, patch-to-parent mapping, per-mosaic annotation coverage and bed/time manifest, a result could be technically executable but scientifically uninterpretable. Exact published baseline reproduction is also unsupported.

## Reproducibility decision

- RD-GuideNet exact reproduction: `NOT_VERIFIED`; custom RGB-D processing and tracking implementation evidence is incomplete.
- YOLOv8-seg exact reproduction: `NOT_VERIFIED`.
- YOLO11-seg exact reproduction: `NOT_VERIFIED`.
- Approximate new RGB-only implementation: `TECHNICALLY_PLAUSIBLE_BUT_NOT_AUTHORIZED`.
- Published split reproduction: `NO_CURRENT_EVIDENCE`.

The existence of pretrained frameworks does not close dataset-membership or evaluation-provenance gaps.

## Leakage decision

Leakage risk is `HIGH` for random image, instance or patch splits because successive frames repeatedly observe the same beds and mushrooms. A patch split also risks distributing content from one parent image across partitions. The 3445/916 instance totals do not demonstrate a safe split.

No split is created or approved here.

## Engineering comparison

### Against C03

C05 advantages:

- exact versioned dataset identity and CC BY 4.0 metadata;
- explicit temporal cadence and acquisition system;
- RGB/depth/COCO structure;
- directly reported segmentation and tracking baselines.

C05 remaining limitations:

- no canonical benchmark membership;
- repeated-scene dependence;
- only two beds and one reported growth cycle;
- baseline environment and split details incomplete.

C05 is more manageable than C03 for a narrowly bounded segmentation study, but does not yet solve the independence/evaluation problem.

### Against C04

C05 appears more manageable because C04 still requires a large payload audit, augmentation-lineage reconstruction, count reconciliation and resolution of paper/code hyperparameter conflicts. C05's RGB-only path is narrower, but its missing manifests still block a defensible capstone benchmark.

## Conditions that would be needed to reconsider

A future, separately authorized decision could reconsider `HOLD` only with evidence such as:

1. authoritative complete file inventory with checksums/version;
2. explicit mapping of 129 release mosaics to the 128 analysis sequence;
3. exact 12 benchmark filenames;
4. image and patch split manifests with parent mapping;
5. COCO `images`/`annotations` coverage reconciliation;
6. record-level bed and time/acquisition identifiers;
7. exact Ultralytics/model versions, configuration, seeds and checkpoint provenance;
8. a capstone estimand explicitly limited to evidence the design can support.

These are conditions, not authorization for another pass in WP-05.

## Final gates

- Recommendation: `HOLD`
- `GO_FOR_DEEP_QC`: `NO`
- Dataset selected: `NO`
- Training authorized: `NO`
- Research gap validated: `NO`
- Full dataset downloaded: `NO`
- Split generated: `NO`
- Historical reports changed: `NO`
- New C05 outputs committed: `NO`
