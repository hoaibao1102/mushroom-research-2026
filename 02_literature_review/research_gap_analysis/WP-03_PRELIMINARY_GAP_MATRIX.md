# WP-03 preliminary gap matrix

Research gap validated: NO. At most two hypotheses per candidate; not preregistered experiments.

| Candidate | Hypothesis | Classification | Already addressed / required next evidence |
|---|---|---|---|
| C03 | Farm/specimen-grouped external evaluation may reduce optimistic validation results. | OBSERVED_EVALUATION_WEAKNESS | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C03 | Field illumination robustness of low-compute disease classifiers may be insufficient. | AUTHOR_STATED_LIMITATION | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C04 | Parent-image- and farm-grouped validation may differ from reported split metrics. | POSSIBLE_RESEARCH_GAP | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C04 | Temporal maturity assessment is not covered by current annotations. | AUTHOR_STATED_LIMITATION | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C05 | Time/trajectory-blocked evaluation may expose same-bed dependency. | POSSIBLE_RESEARCH_GAP | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C05 | Geometry/learned hybrid may improve boundary and tracking balance with lower cost. | AUTHOR_STATED_LIMITATION | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C07 | Asset-disjoint synthetic-to-real evaluation may differ from current result. Simple synthetic pretraining is already evaluated in SMS3D Table5. | POSSIBLE_RESEARCH_GAP | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |
| C08 | Bed/scene-disjoint small-detector evaluation may differ from image-random results; reconcile release first. | POSSIBLE_RESEARCH_GAP | Later searches bounded; verify parent/bed/farm grouping and subsequent literature before novelty claims. |

## Prior-work constraints
- SMS3D Table5 already evaluates synthetic pretraining followed by M18K fine-tuning: simple synthetic-to-real transfer is GAP_ALREADY_ADDRESSED.
- C04 already compares lightweight YOLO architectures and augmentation. Merely trying a lightweight detector or augmentation is not established novelty.
- RD-GuideNet2026already covers depth-guided segmentation and temporal tracking: proposing those alone is GAP_ALREADY_ADDRESSED.
- C06 has INSUFFICIENT_EVIDENCE for a research-gap hypothesis. C03 no-independent-test wording is an observed evaluation weakness, not proof a new grouped test will yield improvement.
- Candidate-specific author limitations and full-text locators remain in source dossiers; no later-paper search proves absence. Do not promote future work to validated novelty.

## Evidence and search scope
Primary source evidence is in WP-03_SOURCE_EVIDENCE.csv and the two stream candidate dossiers/ledgers under source_verification/wp03_stream_a and wp03_stream_b. Stream reports include source links, exact quotes, access logs, full-text scope and later-paper searches. Dataset counts and metrics here are source-reported, not independently inspected image counts or reproduced results. Metadata/HTTP access does not establish payload integrity. No image datasets, weights or training were acquired/executed. Article, code and data licenses are separate.

Searches targeted2024–2026 with DataCite/Zenodo/Mendeley, publisher full text/Crossref and author repositories. Broad DataCite queries sometimes exceeded100records; search coverage is bounded, not systematic completeness. MDPI HTML403 recovered via lawful publisher XML/PDF; Crossref429/network failures recorded. Browser profile locked; HTTP alternatives used. Later-work searches are incomplete/noisy; no global absence or novelty claim. Both streams found RGB-D8n6nr43gk3; it is deduplicated as C05. C01/C02 are not new; excluded hf55tkx489 never acquired. Different identifiers do not establish image-level independence; collection-source overlap still needs audit.
