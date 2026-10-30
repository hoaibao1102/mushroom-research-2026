# WP-04B — C03 Scientific Readiness Report

**Date:** 2026-10-30  
**Branch:** `research/wp-04b-c03-readiness`  
**Decision:** `CONDITIONAL_GO`  
**Training authorization:** `NO`  
**Dataset selection:** `PENDING`  
**Research gap:** `UNVALIDATED`

## Executive finding

C03 có integrity và source traceability đủ để tiếp tục một work package đóng evidence, nhưng chưa đủ để training hay tuyên bố independent biological generalization. Bounded review bác bỏ việc dùng ordinal filename làm specimen ID. Paper cung cấp baseline white-light hữu ích nhưng exact reproduction không khả thi; protocol mới phải được công bố là `NEW_PROTOCOL`.

## Git checkpoint

WP-04 được preserve ở commit `eda47d260aca1db6314b80c4f2a863c9e97a70b9` và remote branch `origin/research/wp-04-deep-verification` đã read-back cùng SHA. Checkpoint gồm 61 project-generated files; không chứa raw JPEG, ZIP/RAR, PDF, model binary, publisher full HTML/text hay C04 `static_text` source copies. Bốn C04 third-party evidence paths còn local-untracked và không được đưa vào checkpoint.

## Task A — identity/grouping

- Không specimen/session/farm IDs hoặc EXIF.
- 120 bounded pairs, 15 strata; 90 equal ordinal + 30 shifted controls.
- AI screening: overall SAME 20, LIKELY 28, DIFFERENT 63, UNCERTAIN 9.
- Equal ordinal: 16 SAME nhưng 48 DIFFERENT; controls vẫn 4 SAME.
- Human adjudication chưa có; hard grouping edge = 0.
- Kết luận: `BIOLOGICAL_INDEPENDENCE_NOT_VERIFIED`.

## Task B — labels

Năm White folder counts khớp paper. `hl/bb/db/wb` được hỗ trợ bởi count + caption semantics. `kw → Cobweb` là `PROVISIONAL_PARTIALLY_SUPPORTED`, do count 664 khớp nhưng paper dùng token `cw`/Cobweb chứ không giải thích `kw`. Authors report expert mycologist annotation; lab confirmation không được thiết lập.[S1]

## Task C — reproduction

Biết dataset counts, 20 architectures, 80/20, high-level preprocessing, batch 11, LR .001, SGD momentum .9, 8 epochs và weighted score. Thiếu historical manifest/split seed, grouping, exact cleaning, loss/fine-tuning/checkpoint/software versions và metric averaging. Validation vừa tuning/model-selection vừa final reporting, không independent test. Exact reproduction: `NO`; partial reimplementation: `YES`; valid future experiment: `NEW_PROTOCOL_REQUIRED`.

## Task D — protocol

Defensible protocol chỉ khả thi sau complete group evidence. Proposed estimands tách in-domain, cross-light, leave-one-light-out và farm/session holdout. Primary split phải group-aware; sealed test không tham gia selection; train-only preprocessing; report macro/per-class/calibration và group-aware uncertainty. Chưa tạo split.

## Task E — literature prescreen

Bounded review xác nhận original dataset/paper chain, prior Agaricus imaging và transferable domain-shift/group-split/leakage-aware methods. Trong coverage đã rà soát chưa xác nhận independent reuse của Zenodo 20260929 hoặc benchmark C03 đồng thời cross-light + specimen-grouped + leakage-aware. Đây là evidence gap, không phải novelty claim.[S2][S3]

## Decision

`CONDITIONAL_GO` chỉ cho work package đóng provenance/grouping/label evidence. Không authorize training. Stop nếu work package kế tiếp không thể cung cấp complete grouping hoặc estimand trung thực; khi đó đánh giá `NO_GO_FOR_PRIMARY_GENERALIZATION` và chuyển backup.

## Deliverables

1. `setup_reports/WP-04B_READINESS_REPORT.md`
2. `03_dataset_discovery/screening_reports/C03_FINAL_FEASIBILITY_DECISION.md`
3. `03_dataset_discovery/source_verification/C03_SPECIMEN_GROUPING_AUDIT.md`
4. `03_dataset_discovery/source_verification/C03_LABEL_SEMANTICS_AUDIT.md`
5. `02_literature_review/methodology_comparison/C03_PAPER_REPRODUCTION_MATRIX.md`
6. `05_research_protocols/C03_PROPOSED_EVALUATION_PROTOCOL.md`
7. `02_literature_review/research_gap_analysis/C03_GAP_PRESCREEN.md`
8. Candidate-local CSV/index/manifest/15 plates/scripts under `04_dataset_candidates/C03_agaricus_disease/qc/wp04b_readiness/`
9. Validation evidence: `setup_reports/WP-04B_VALIDATION.json`

## Sources

- **[S1]** Albayrak et al. (2025), https://doi.org/10.3390/agronomy15010226.
- **[S2]** Dataset paper (2024), https://doi.org/10.30708/mantar.1452976.
- **[S3]** Zenodo record 20260929, https://zenodo.org/records/20260929.
