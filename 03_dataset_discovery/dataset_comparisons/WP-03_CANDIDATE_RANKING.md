# WP-03 ranking — eligibility first

**Eligible ranking: empty (0/6 meet all mandatory checks).** Do not interpret follow-up priorities as accepted candidates or final topic selection.

| Follow-up priority | Candidate | Rationale | Hard blockers |
|---|---|---|---|
| 1 | C03 disease classification | Existing standard pretrained CNN comparison; relatively manageable single-image task; CC BY dataset declaration | Exact paper subset/version and independent evaluation unresolved |
| 2 | C04 shiitake phenotypes | CC BY data declaration, exact data paper and code archive listed; real cultivation/maturity/defect context | Detection not classification; count/augmentation lineage, farm grouping and split integrity unresolved |
| 3 | C05 RGB-D time-series | Exact version linked in data and method papers; license clear | Higher segmentation/tracking complexity,12mosaic subset, temporal dependence and code gap |
| 4 | C08 M18K | Real farm baseline comparisons and traceable author release | Data license inside uninspected archive; paper/current-release counts and grouped splits unresolved |
| 5 | C07 SMS3D | Author-linked public samples and exact original paper | Data asset rights, full40Kauthor-contact access, synthetic dependence and3Dcomplexity |
| 6 | C06 PDA scans | Oyster growth domain and open metadata | No exact paper, clear classification ground truth or baseline confirmed |

## Scoring policy
Use DATASET_SELECTION_CRITERIA.md0–4anchors/weights only after hard checks. No weighted totals assigned because independent units, leakage, QC and version correspondence remain unknown; do not renormalize unknowns. Verified observations include source identity/article links and declared license where retrieved; engineering difficulty/compute/time judgments remain estimates, not scores backed by benchmarks. This is a follow-up-effort ordering, not an eligible scientific ranking. No quantitative compute/time promise.

## Evidence and search scope
Primary source evidence is in WP-03_SOURCE_EVIDENCE.csv and the two stream candidate dossiers/ledgers under source_verification/wp03_stream_a and wp03_stream_b. Stream reports include source links, exact quotes, access logs, full-text scope and later-paper searches. Dataset counts and metrics here are source-reported, not independently inspected image counts or reproduced results. Metadata/HTTP access does not establish payload integrity. No image datasets, weights or training were acquired/executed. Article, code and data licenses are separate.

Searches targeted2024–2026 with DataCite/Zenodo/Mendeley, publisher full text/Crossref and author repositories. Broad DataCite queries sometimes exceeded100records; search coverage is bounded, not systematic completeness. MDPI HTML403 recovered via lawful publisher XML/PDF; Crossref429/network failures recorded. Browser profile locked; HTTP alternatives used. Later-work searches are incomplete/noisy; no global absence or novelty claim. Both streams found RGB-D8n6nr43gk3; it is deduplicated as C05. C01/C02 are not new; excluded hf55tkx489 never acquired. Different identifiers do not establish image-level independence; collection-source overlap still needs audit.
