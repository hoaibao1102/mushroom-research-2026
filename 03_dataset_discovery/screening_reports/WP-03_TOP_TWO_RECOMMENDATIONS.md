# WP-03 top-two follow-up recommendations

**There are fewer than two fully eligible candidates: zero at present.** The following are conditional investigation priorities, not selected topics.

## 1. C03 — Agaricus disease classification
Source dataset10.5281/zenodo.20260929; paper10.3390/agronomy15010226(2025). Repository explicitly links the paper; classify AUTHOR_LINKED_DATASET, not exact byte/subset equality. Five disease/healthy classes; paper reports3195white-light images and20pretrained CNNs. This is closest to requested manageable classification. Article says no separate test; validation reused. Source deposit addsUV/mixed illumination and appears2026, so request exact paper-subset manifest and grouped labels before any acquisition/score.

## 2. C04 — Shiitake phenotype/growth-stage dataset
Source10.5281/zenodo.20373531; paper10.1038/s41597-026-07754-7(2026), EXACT_DATASET_USED. DatasetCCBY4.0metadata; image/YOLO labels and code archive advertised. Source reports1782original,6500augmented,43752instances, while model partition refers5375images. Stronger relationship but more complex detection, species mismatch and augmentation-parent split risk. Resolve counts, exact archive acquisition method, code license and farm/parent split before approval.

## Approval boundary
Both remain NOT_YET_ELIGIBLE. Source-reported high metrics do not trump independent evaluation. No final topic, model or gap selected. Next package should be targeted source/subset and split verification, not training; switch to additional discovery if blockers cannot be closed efficiently.

## Evidence and search scope
Primary source evidence is in WP-03_SOURCE_EVIDENCE.csv and the two stream candidate dossiers/ledgers under source_verification/wp03_stream_a and wp03_stream_b. Stream reports include source links, exact quotes, access logs, full-text scope and later-paper searches. Dataset counts and metrics here are source-reported, not independently inspected image counts or reproduced results. Metadata/HTTP access does not establish payload integrity. No image datasets, weights or training were acquired/executed. Article, code and data licenses are separate.

Searches targeted2024–2026 with DataCite/Zenodo/Mendeley, publisher full text/Crossref and author repositories. Broad DataCite queries sometimes exceeded100records; search coverage is bounded, not systematic completeness. MDPI HTML403 recovered via lawful publisher XML/PDF; Crossref429/network failures recorded. Browser profile locked; HTTP alternatives used. Later-work searches are incomplete/noisy; no global absence or novelty claim. Both streams found RGB-D8n6nr43gk3; it is deduplicated as C05. C01/C02 are not new; excluded hf55tkx489 never acquired. Different identifiers do not establish image-level independence; collection-source overlap still needs audit.
