# C05 Final Preflight Report

## Audit boundary

- Audit date: 2026-10-30
- Candidate: C05
- Dataset: `10.17632/8n6nr43gk3.1`
- Method paper: `10.3390/s26061935`
- Data-description paper: `10.1016/j.dib.2026.113085`
- Audit type: one bounded source/metadata-only pass
- Full dataset downloaded: `NO`
- Model training or implementation: `NO`
- Split generated: `NO`
- Dataset selected: `NO`
- Training authorized: `NO`
- Research gap validated: `NO`
- DS-02 reused: `NO`

## Executive decision

**C05 decision: `HOLD`.**

C05 is suitable for further scientific exploration because its public record establishes an RGB-D temporal acquisition, COCO-format instance annotations, a CC BY 4.0 licence, and a directly related method paper. It is **not yet suitable as the selected capstone dataset or as authority to train**, because the public metadata inspected in this pass does not expose the exact 12-image benchmark membership, image/patch train-test manifests, per-mosaic annotation coverage, a canonical 129-to-128 reconciliation, or explicit bed membership sufficient for a defensible evaluation protocol.

The evidence therefore does not meet the rule for `GO_FOR_DEEP_QC`. This `HOLD` does not reject the dataset scientifically; it prevents an unsupported capstone commitment.

## Verified source findings

| Status | Finding | Evidence |
|---|---|---|
| FACT | Dataset DOI/version identity is `10.17632/8n6nr43gk3.1`; DataCite identifies Mendeley Data as publisher. | Saved DataCite record. |
| FACT | Public Mendeley metadata displays CC BY 4.0. | Saved Mendeley record. |
| AUTHOR_REPORTED | The release contains 129 stitched RGB-depth mosaics generated from 17 overlapping RGB-D frames per time point at 10-minute intervals. | Mendeley dataset description. |
| AUTHOR_REPORTED | RGB, corresponding depth maps and mushroom-cap instance masks in COCO format are release components. | Mendeley dataset description. |
| AUTHOR_REPORTED | The method paper used 128 stitched mosaics as segmentation/tracking inputs across one growth cycle, collected 18–21 March 2025. | Method paper, Section 2.1. |
| AUTHOR_REPORTED | The method paper used 12 RGB mosaics for the YOLO segmentation benchmark, split them into 256 × 128 patches, and reports 4361 annotated instances: 3445 training and 916 testing. | Method paper, Section 2.4. |
| AUTHOR_REPORTED | YOLOv8-seg and YOLO11-seg used pretrained weights, 256 × 256 input, Adam with learning rate 0.01, batch 32 and 50 initial epochs; additional training was 30 and 20 epochs respectively. | Method paper, Section 2.4. |
| AUTHOR_REPORTED | Two production beds were imaged by a fixed rail-mounted ZED Mini system. | Method paper, Section 2.1. |
| FACT | The public naming description is `YYYYMMDD_cycleXX`; `cycleXX` represents 10-minute intervals. | Mendeley reproduction notes. |
| NOT_VERIFIED | Exact released filenames and checksums for all 129 mosaics. | Public file tree did not resolve in the bounded metadata capture; no payload was downloaded. |
| NOT_VERIFIED | Why the paper has 128 mosaics while the release says 129. | Neither inspected source identifies the additional/omitted mosaic or states a reason. |
| NOT_VERIFIED | Identities of the 12 YOLO benchmark mosaics. | No filename list or benchmark manifest was found in inspected sources. |
| NOT_VERIFIED | Train/test image membership or patch-to-parent mapping. | The paper reports instance totals, not a manifest. |
| NOT_VERIFIED | COCO coverage for every one of the 129 mosaics. | The release describes COCO annotations globally but no per-file coverage inventory was available in this pass. |
| NOT_VERIFIED | A bed identifier in each filename/annotation record. | Date/cycle naming is documented; bed membership is not. |
| NOT_VERIFIED | Exact Ultralytics versions, model variant sizes, seeds, augmentation settings, patch inclusion rules and released `best.pt` weights. | Not specified or recoverable from inspected metadata/full text. |

`AUTHOR_REPORTED` means a claim appears in the primary dataset or paper record but was not independently checked against the complete payload in this audit.

## Reconciliation of 129 / 128 / 12

The three values refer to different reported scopes:

1. **129** — release-level count of stitched RGB-D mosaics.
2. **128** — method-paper temporal sequence used for segmentation/tracking analysis.
3. **12** — RGB mosaics selected for the YOLO benchmark and manual polygon annotation workflow.

It is an **INFERENCE** that 12 likely belongs to the broader temporal acquisition because the paper says the models use preprocessed RGB mosaics described in Section 2.1. It is **not verified** that those 12 are an identifiable subset of either the 128-paper sequence or the 129-release set. It is also **not verified** that 128 equals 129 minus one particular file. Possible exclusion, acquisition, processing or version explanations are not evidence and are therefore not adopted.

These numbers count images/mosaics or task subsets, **not independent biological samples**.

## Reproducibility assessment

### What can be scoped

- RGB-only instance segmentation is technically definable.
- Patch dimensions and headline YOLO training parameters are author-reported.
- COCO-compatible tooling and Ultralytics implementations are publicly available in principle.
- The licence metadata supports research reuse with attribution.

### What cannot yet be reproduced exactly

- exact 12 parent mosaics;
- image-level and patch-level split membership;
- deterministic patch extraction, edge handling and empty-patch policy;
- model scale/checkpoint identity and exact package versions;
- random seeds and augmentation configuration;
- mapping of 3445/916 instances to parent mosaics and patches;
- historical trained weights or a runnable experiment manifest;
- exact evaluation sample used for the published metrics.

Result: **approximate reimplementation is plausible; exact YOLOv8-seg/YOLO11-seg reproduction is `NOT_VERIFIED`.**

## Leakage and evaluation risk

Consecutive mosaics observe the same beds at 10-minute intervals. Random image or random patch splitting can place near-adjacent views of the same scene and repeatedly observed mushrooms on both sides of a split. Patch splitting can additionally place patches from one parent mosaic into both train and test. The reported 3445/916 instance totals do not establish leakage-safe grouping.

An honest protocol would require grouping at least by parent mosaic before patching and preferably by defensible time block or acquisition unit. A forward-time evaluation may be possible because date/cycle order is documented, but its exact construction is currently blocked by missing canonical membership and by the small number of acquisition days. A bed-aware evaluation is `NOT_VERIFIED` because per-record bed IDs were not established; with only two beds, even a verified bed holdout would provide limited evidence about generalization.

## Engineering complexity

| Area | Assessment |
|---|---|
| Data access/licence | Manageable in principle; CC BY 4.0 metadata is present. |
| RGB-only model pipeline | Moderate once manifests are available. |
| RGB-D/RD-GuideNet reproduction | High: custom stitching, depth geometry, segmentation and temporal tracking are involved. |
| Leakage-safe benchmark reconstruction | High under current evidence because parent/subset/split manifests are missing. |
| Storage/compute | Likely more manageable than C04, but payload size/file inventory was not verified in this pass. |
| Scientific independence | Limited: one facility, one four-day cycle and two beds are author-reported. |

Compared with C03, C05 has clearer temporal acquisition, annotation format, licence and dataset-paper identity, but it still lacks a defensible public split/group manifest. Compared with C04, C05 appears narrower and more directly traceable, while C04 retains unresolved payload, lineage, count and paper/code conflicts. Therefore C05 remains the most manageable fallback **for bounded clarification**, not an approved experiment.

## Narrowed RGB-only objective

A scientifically meaningful narrow objective could be: evaluate RGB-only cap instance segmentation under explicitly parent-grouped and temporally ordered validation, reporting boundary accuracy and failure modes in dense/occluded regions. This is meaningful only if the study tests an acquisition/evaluation claim such as temporal robustness or dense-boundary reliability. Merely swapping YOLO architectures is not a validated research contribution.

The objective remains conditional on recoverable parent membership, leakage-safe grouping and a declared estimand. It cannot be approved from current metadata alone.

## Exact blockers

1. No canonical mapping among 129 release mosaics, 128 tracking mosaics and 12 benchmark mosaics.
2. No explanation identifying the 129-to-128 discrepancy.
3. No public filename list for the 12 benchmark mosaics in the inspected evidence.
4. No image/patch train-test manifest or patch-to-parent mapping.
5. No per-mosaic COCO annotation coverage inventory.
6. No verified bed identifier per mosaic/annotation record.
7. No exact baseline environment: Ultralytics version, model sizes, seeds, augmentation and patch policies.
8. No verified released training checkpoints/configuration sufficient for exact reproduction.
9. Only one four-day growth cycle and two beds are author-reported, limiting external-generalization claims.

## Stop state

- Recommendation: `HOLD`
- Scientific exploration suitability: `CONDITIONAL_YES`
- Capstone selection suitability: `NO_NOT_YET`
- Dataset selected: `NO`
- Training authorized: `NO`
- Research gap validated: `NO`
- Further source passes in this work package: `NO`
