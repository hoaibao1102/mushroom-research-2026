# WP-03 discovery report

Status: CONDITIONAL discovery completed; no selection. Six distinct plausible new dataset leads; five have identified paper links, of which 4 are EXACT_DATASET_USED and one AUTHOR_LINKED_DATASET. C06 is a weaker adjacent lead with no exact paper confirmed, retained transparently rather than counted as a pair. **Zero candidates currently satisfy every mandatory eligibility criterion**. At least two fully eligible recommendations cannot be provided honestly.

| ID | Dataset | Relationship | Blocking uncertainty |
|---|---|---|---|
| C03 | Comprehensive Image Dataset of Agaricus bisporus Diseases Under Controlled Illumination Conditions | AUTHOR_LINKED_DATASET | Author-linked multi-illumination deposit vs white-light paper subset unresolved; validation reused; no independent test |
| C04 | Phenotypic image dataset of naturally grown shiitake mushrooms across multiple varieties and growth stages | EXACT_DATASET_USED | 1782/6500/5375 count/subset and augmentation-parent split accounting unresolved; quantitative validation only |
| C05 | RGB-D Time-Series Dataset of White Button Mushroom Growth for Instance Segmentation | EXACT_DATASET_USED | 12-mosaic method subset vs129 deposit; grouped independence and runnable method code unresolved; higher complexity |
| C06 | Scanned images of Oyster mushroom's mycelium grown on a PDA medium | UNVERIFIED | No exact paper, explicit ML label schema, reported image count or reproducible predictive baseline confirmed |
| C07 | SMS3D: 3D Synthetic Mushroom Scenes Dataset | EXACT_DATASET_USED | Dataset asset license/version/access and grouped split not closed |
| C08 | M18K real-world mushroom detection, pose and growth dataset | EXACT_DATASET_USED | Dataset asset license/version/access and grouped split not closed |

## Candidate details (20-field coverage)
The new-candidate CSV contains authors/platform, persistentID/canonicalURL/version/date/license/access, reportedcounts, labels/method, original/derived provenance, exactpaper, relation, baseline/results/evaluation, code, leakage, compute, farm relevance and limitations. It retains original stream records, including discrepancies, rather than forcing compatible counts. Detailed original source dossiers are not dataset folders.

C03 is the closest manageable classification lead, but its deposited white/UV/mixed archive has not been equated to the2025paper's3195white-light images. C04 is a real shiitake detection dataset, not oyster classification;6500augmented vs5375partition images and parent grouping require clarification. C05 has real temporal RGB-D but higher complexity and limited independent beds. C07 synthetic assets/licensing and full-release access are unresolved. C08 main/growth versions have count and license discrepancies. C06 laboratory mycelium scans need a clear predictive task and paper.

## Evidence and search scope
Primary source evidence is in WP-03_SOURCE_EVIDENCE.csv and the two stream candidate dossiers/ledgers under source_verification/wp03_stream_a and wp03_stream_b. Stream reports include source links, exact quotes, access logs, full-text scope and later-paper searches. Dataset counts and metrics here are source-reported, not independently inspected image counts or reproduced results. Metadata/HTTP access does not establish payload integrity. No image datasets, weights or training were acquired/executed. Article, code and data licenses are separate.

Searches targeted2024–2026 with DataCite/Zenodo/Mendeley, publisher full text/Crossref and author repositories. Broad DataCite queries sometimes exceeded100records; search coverage is bounded, not systematic completeness. MDPI HTML403 recovered via lawful publisher XML/PDF; Crossref429/network failures recorded. Browser profile locked; HTTP alternatives used. Later-work searches are incomplete/noisy; no global absence or novelty claim. Both streams found RGB-D8n6nr43gk3; it is deduplicated as C05. C01/C02 are not new; excluded hf55tkx489 never acquired. Different identifiers do not establish image-level independence; collection-source overlap still needs audit.
