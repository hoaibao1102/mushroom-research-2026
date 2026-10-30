# WP-01 C01: primary-source and related-paper verification

## Scope and decision

Access date: 2026-10-23 (timestamps in `access_search_log.jsonl` are UTC). This package is metadata/public-text only. It does not contain dataset payloads, archives, images, weights, training runs, or imported DS02 artifacts. Only this new evidence directory was written; shared registries, git, and other reports were not changed.

**G0 recommendation: CONDITIONAL / HOLD for dataset acceptance; training authorization: NOT_AUTHORIZED.** Identity, version history and declared license are established, and task relevance is plausible. Biological truth, sample independence and split feasibility remain unresolved. This is an evidence-gap assessment, not a declaration that the dataset is unsuitable or that no prior work exists. A payload audit would require separate authorization; it was deliberately not performed here.

## C01 identity, rights and version history

The v2 landing page identifies **Mushroom Disease Dataset (Healthy, Single Infected & Mixed Infected)**, DOI **10.17632/jrbx34k77g.2**, published **30 June 2025**, with contributors **Abdullah Mazumdar; Jubayer Ahmed Bhuiyan Shawon; Sumon Debnath; Md Abdullah**. The same creators and publication year are present in the DataCite registration.[1][4]

The landing page declares **CC BY 4.0**; DataCite explicitly registers `Creative Commons Attribution 4.0 International` / `cc-by-4.0`. This verifies a repository license declaration, not ownership of every image or third-party permissions. The embedded license text also cautions that further permission may be required for content identified as third-party.[1][4]

The public versions endpoint lists v1 published **2025-06-16** and v2 published **2025-06-30**, both `available:true`.[6] The v1 title is **Mushroom Disease Dataset (Healthy, Black Mold & Green Mold)**, whereas its description already uses healthy/single-infected/mixed-infected semantics. Therefore a v1 title must not be substituted for v2 class definitions.[2][5]

Version counts are source-reported, not audited: v1 says **680** images (**299 healthy, 72 single-infected, 309 mixed-infected**); v2 says **761** (**299, 147, 315**, respectively).[1][2] The metadata change does not prove that only new images were added, that old images were unchanged, or that labels remained stable. No file-level version diff was obtained.

DataCite v2 `Issued` is `2025-06-30T17:00:11Z`, registry `updated` is `2025-06-30T17:00:14.000Z`; the repository embedded snapshot has `publish_date=2025-06-30T17:00:11.898Z` and `last_modification_date=2025-06-27T09:39:02.988Z`. These fields have different roles; do not silently treat registry update time as acquisition time.[1][4]

## What the source actually says about the data

Verbatim v2 description excerpt:

> “Mushroom cultivation bags, categorized into healthy, single-infected, and mixed-infected classes, were photographed at the Mushroom Development Institute in Savar, Dhaka, Bangladesh.”[1]

> “The dataset comprises a total of 761 high-resolution images, including 299 healthy samples, 147 single-infected samples, and 315 mixed-infected samples.”[1]

> “The mixed-infected category represents bags affected by multiple pathogens or overlapping infection patterns, typically involving both types of mold.”[1]

> “All images were originally captured in HEIC format using an iPhone 11 Pro Max and were later converted to JPG format for standardization and broader compatibility.”[1]

All of these are **REPORTED_BY_SOURCE_NOT_AUDITED** dataset-content claims. Neither landing metadata nor its duplicate DataCite abstract is an independent count, pathology assay, file inspection, or independent corroborating study.[1][4]

The description associates contamination with green mold, black mold or both; it does **not** give organism identifications, culture/PCR/microscopy criteria, expert adjudicator identities, agreement measurements, or operational rules separating “single” from “mixed.” In particular, “typically” and “overlapping infection patterns” do not warrant equating every mixed label to laboratory-confirmed co-infection.[1] Current biological-confirmation status: **UNVERIFIED**.

The described observation is a cultivation bag image, not an edible/poisonous species label, mushroom maturity target, or fruit-body disease-localization annotation. Treat this as a candidate image-classification task, not a confirmed detection dataset. This is a reviewer interpretation of the description, not a payload audit.[1]

## Files, labels, groups and splits: unresolved, not fabricated

The saved landing HTML includes a `Files` heading but its embedded state is still `filesLoading:true`, `foldersLoading:true` with empty arrays. The public files request with `folder_id=root&version=2` returned `[]`; without `folder_id` it returned HTTP 200 but body `{"error":400}`. Several alternative metadata endpoints returned 404. These responses do **not** establish that the deposited dataset is empty.[1][22]

Consequently archive names, sizes, checksums, complete file list, directory hierarchy, literal folder names, filename-to-label mapping, per-file labels and any README contents are **UNVERIFIED**. No archive or image was downloaded to work around this boundary. The HEIC-to-JPG statement is a source description, not an observed inventory.[1]

No bag IDs, repeated-view linkage, collection dates, session/batch IDs, cultivation cycles, farms beyond the stated institute, independent unit count, split ratios or predefined train/validation/test manifests were found in the retrieved C01 description/registration. Thus independence, leakage-free splitting and generalization beyond the collection site are unresolved. Metadata subject tags such as “Data Augmentation” and “Transfer Learning” are not evidence that augmentation or a specific model was actually used.[1][4]

Before unconditional G0 acceptance, request: (1) a version-pinned file/label manifest; (2) operational class definitions and biological or expert confirmation protocol; (3) bag/session/batch identifiers and repeated-view relationships; (4) acquisition dates and sites; (5) a documented group-disjoint split protocol; (6) explanation of v1→v2 content/label changes; (7) authoritative related-paper link if one exists. Keep source-reported image counts distinct from unique bags and independently audited files.

## Exact-DOI citation search

Exact v2 DOI, dataset stem and title variants were searched through Crossref, OpenAlex and web search; raw responses and failed queries are preserved. OpenAlex stem search returned `meta.count=0`; the successful retried Crossref stem query returned zero items. Crossref's initial exact-DOI free-text query instead returned unrelated works, which were not promoted into citations. Free-text APIs are not exhaustive cited-reference indexes.[9][19][40]

Bing returned conspicuously unrelated results (TikTok, transport pages, general mushroom definitions) despite exact-token queries. Google HTTP 200 pages were JavaScript/redirect shells, not usable scholarly search results. Their apparent success is not substantive search coverage.[10][12][23][24] Some Crossref requests initially returned HTTP 429; a later serial/broader request succeeded.[26][40]

**No exact-C01-DOI paper citation or direct reuse was confirmed within this search.** This is not a proof of absence, a comprehensive citation count, or a novelty claim. C01 `related_links` in the repository snapshot and DataCite `relatedItems` are empty; DataCite related identifiers only connect to the dataset's concept DOI.[1][4] No primary source tied a paper to C01.

## Related 2024–2026 papers: bounded screening

### Direct same-task prior work: Bacanto et al., 2026

**John Rovic D. Bacanto; Joed Michael Meraña; Channa Marie Gabrielle Simbajon; Mark Reden S. Pacaon.** *Hybrid Feature Engineering and Artificial Neural Network for Mushroom Fruiting Bag Contamination Classification*. 2026 International Conference on Frontiers of Engineering and Emerging Technologies (FET), publication date **2026-04-22**, DOI **10.1109/FET68771.2026.11601212**.[27]

Review scope: **ABSTRACT_ONLY**. The ordinary IEEE document URL returned a bot-verification shell, but the lawful `/abstract/document/11601212` alternative returned the full abstract in HTML `meta[property="og:description"]` and `twitter:description`. That abstract is saved separately as text, with original HTML retained.[32][36]

> “Accordingly, a dataset comprising healthy, green mold, black mold fruiting bags was collected from mushroom farms in Laguna. Images were captured from multiple angles using an iPhone 15 and subsequently validated by experienced mushroom growers and agricultural experts to ensure accurate class representation.”[36]

The abstract reports modified ResNet-18 + CBAM deep features combined with GLCM handcrafted texture features, an ANN classifier, 100 epochs and overall accuracy **86.9%**. These are author-reported abstract claims, not reproduced results; full split design, dataset size and uncertainty were not established.[36]

Relationship: **SAME_TASK_DIFFERENT_DATASET**, supported by the explicit Laguna/iPhone 15 collection versus C01's Savar/iPhone 11 Pro Max account. Crossref's deposited reference list does not contain the C01 DOI/stem, but registry references are not a full-text bibliography audit.[1][27][36] This paper defeats an unqualified assertion that fruiting-bag contamination classification has no prior work; it does not close C01 provenance or establish a comparable performance benchmark.

### Contamination-related culture work: Ujir et al., 2024

**Hamimah Ujir; Irwandi Hipiny; Mohamad Hasnul Bolhassan; Ku Nurul Fazira Ku Azir; SA Ali.** *Automating Mushroom Culture Classification: A Machine Learning Approach*. IJACSA **15(4)**, **2024**, DOI **10.14569/IJACSA.2024.0150454**.[28][33]

Review scope: **ABSTRACT_ONLY** (publisher page and bibliographic metadata; article PDF not retrieved under this metadata-only package). The abstract says **1400 images**, **two Pleurotus ostreatus strains**, **14 days**, using HSV histogram and CNN-based approaches (MNet/MConNet), with reported average accuracies **92.15% growth prediction** and **97.81% contamination prediction**.[33] It establishes related culture-contamination research, not the same substrate-bag three-class construct or C01 reuse. Do not compare that abstract accuracy to a future C01 result without protocol and dataset compatibility review.

A 2026 book chapter with the same title (DOI **10.58532/NBENNURNGCDB1P1C2**) was also discovered; retrieved OpenAlex abstract repeats the 1400-image/two-strain/14-day and reported accuracy account. Crossref metadata is saved. It is a related lead, **not counted as independent experimental confirmation** without full text and relationship review.[25][39]

### Additional disease-related leads, not confirmed substrate-bag studies

- **Shilpashree P S; Chandru V; Shrishail Lagali; Ramesh G N; Chetan D.** *Automated Disease Detection in Oyster Mushroom Cultivation Using Deep Learning Technique*, ICSSES, **2025-03-21**, DOI **10.1109/ICSSES64899.2025.11009558**. **Metadata only**: dataset, target and bag-contamination relevance unresolved; no C01 relationship established.[29]
- **Tanvi Yadav; Shivanshi Sharma; Kavneet Kaur; Vikas Upadhyaya.** *IoT-Based Automated Mushroom House with Early-Stage Disease Detection*, ICAISET, **2026-04-21**, DOI **10.1109/ICAISET66439.2026.11542036**. **Metadata only**: not a verified C01 or substrate-bag benchmark.[30]
- **Isabelino Jr. Paat.** *Mushroom Disease Detection and Classification with Decision Support*, The Light Explorer, **2024-09-01**, DOI **10.57180/NGMD7490**. **Metadata only**; publisher URL failed DNS. Methods, target and data remain unresolved.[31]

The machine-readable `related_papers.csv` preserves complete retrieved author names, access scope, task relevance and dataset relationship separately. Other search results about species toxicity, shelf life, fruit-body detection and biological mold control were not treated as same-task benchmarks. Search coverage is exploratory, not systematic.

## Excluded DS02: metadata-only comparison

**Annotated Oyster Mushroom Images**, DOI **10.17632/hf55tkx489.1**, publication **2024-07-15**, contributors **Sonay Duman; Abdullah Elewi; Abdulsalam Hajhamed; Rasheed Khankan; Amina Souag; Asma Ahmed**, repository-declared CC BY 4.0.[3][8]

The abstract reports **555 raw camera images**, about **8,000 mushroom-labeled** and over **8,000 maturity-labeled images**, annotations and environmental sensor data, collected over two cultivation cycles in Mersin, Turkey.[8] Those are source claims, not audited payload counts here. DS02's detection/maturity/sensor framing is different from C01's bag-contamination classes. It remains **EXCLUDED**; metadata comparison does not reopen it. No DS02 files, archives, labels, prior local artifacts or model outputs were imported.

## Failures and verification boundaries

`requests` was unavailable, so retrieval used standard-library `urllib`; no installation was needed. Browser fallback was blocked by a locked Chrome profile; no browser was closed or configuration changed. Primary pages and JSON were nevertheless retrieved successfully via urllib. File metadata endpoints had 404/empty/error-body results; web search had noisy/unusable results; one publisher DNS lookup failed. All network attempts and their outcomes are logged.

`verification.json` checks CSV schema/status vocabulary, required artifact existence, exact DOI formats, source hashes, and citation-ledger consistency. It is structural/provenance verification, not independent scientific validation or file-count auditing.

## Sources

[1] https://data.mendeley.com/datasets/jrbx34k77g/2 — c01_v2
    > "The dataset comprises a total of 761 high-resolution images, including 299 healthy samples, 147 single-infected samples, and 315 mixed-infected samples."
[2] https://data.mendeley.com/datasets/jrbx34k77g/1 — c01_v1
    > "The dataset comprises a total of 680 high-resolution images, including 299 healthy samples, 72 single-infected ones, and 309 mixed-infected images."
[3] https://data.mendeley.com/datasets/hf55tkx489/1 — excluded_ds02_v1
    > "Annotated Oyster Mushroom Images"
[4] https://api.datacite.org/dois/10.17632/jrbx34k77g.2 — c01_datacite_v2
    > "Creative Commons Attribution 4.0 International"
[5] https://api.datacite.org/dois/10.17632/jrbx34k77g.1 — c01_datacite_v1
    > "Mushroom Disease Dataset"
[6] https://data.mendeley.com/public-api/datasets/jrbx34k77g/versions — c01_versions_api
    > "[
  {
    "version": 1,
    "publish_date": "2025-06-16",
    "available": true
  },
  {
    "version": 2,
    "publish_date": "2025-06-30",
    "available": true
  }
]"
[8] https://api.datacite.org/dois/10.17632/hf55tkx489.1 — ds02_datacite
    > "Annotated Oyster Mushroom Images"
[9] https://api.crossref.org/works?query=%2210.17632%2Fjrbx34k77g.2%22&rows=12&filter=from-pub-date%3A2024-01-01%2Cuntil-pub-date%3A2026-12-31 — search_crossref_exact_doi
    > "[
  "title 17632"
]"
[10] https://www.bing.com/search?q=%2210.17632%2Fjrbx34k77g.2%22 — search_bing_exact_doi
    > "TikTok - Make Your Day"
[12] https://www.bing.com/search?q=%22jrbx34k77g%22 — search_bing_exact_stem
    > "Bến xe Miền Tây"
[19] https://api.openalex.org/works?search=%22jrbx34k77g%22&per-page=20 — search_openalex_exact
    > "{
  "meta": {
    "notice": "No API key, so this request shares one free daily budget ($0.10) with everyone on your network's IP address. Get a free key with its own $1/day at https://openalex.org/settings/api and add api_key=YOUR_KEY to your requests. An AI agent can get one for its user in one call: POST https://api.openalex.org/api-keys with {\"email\": \"<your user's email>\"}; we email them a link, and the key works once they click it. Docs for agents: https://help.openalex.org/llms.txt",
    "count": 0,
    "db_response_time_ms": 9,
    "page": 1,
    "per_page": 20,
    "groups_count": null,
    "x_query": {
      "oql": "get works where full text has (stemmed \"jrbx34k77g\")",
      "x_new_oql": "get works with (stemmed \"jrbx34k77g\") in the full text",
      "oqo": {
        "get_rows": "works",
        "filter_rows": [
          {
            "column_id": "fulltext.search",
            "value": "\"jrbx34k77g\"",
            "operator": "has"
          }
        ]
      },
      "url": "/works?filter=fulltext.search:%22jrbx34k77g%22&per_page=20"
    },
    "cost_usd": 0.001
  },
  "results": [],
  "group_by": []
}"
[22] https://data.mendeley.com/public-api/datasets/jrbx34k77g/files?version=2 — c01_files_no_folder
    > "{
  "error": 400
}"
[23] https://www.google.com/search?q=%22jrbx34k77g%22 — google_exact
    > "Nếu bạn gặp vấn đề khi truy cập vào Google Tìm kiếm"
[24] https://www.google.com/search?q=mushroom+bag+contamination+classification+2025+2026 — google_related
    > "Nếu bạn gặp vấn đề khi truy cập vào Google Tìm kiếm"
[25] https://api.openalex.org/works?search=mushroom+contamination+classification&filter=from_publication_date%3A2024-01-01%2Cto_publication_date%3A2026-10-23&per-page=30 — openalex_bags
    > "Automating Mushroom Culture Classification"
[26] https://api.crossref.org/works?query.title=mushroom+contamination+detection&rows=30&filter=from-pub-date%3A2024-01-01%2Cuntil-pub-date%3A2026-10-23 — crossref_bags_retry
    > "Hybrid Feature Engineering"
[27] https://api.crossref.org/works/10.1109/fet68771.2026.11601212 — paper_1_crossref
    > "Hybrid Feature Engineering"
[28] https://api.crossref.org/works/10.14569/ijacsa.2024.0150454 — paper_2_crossref
    > "Automating Mushroom Culture Classification"
[29] https://api.crossref.org/works/10.1109/icsses64899.2025.11009558 — paper_3_crossref
    > "Automated Disease Detection"
[30] https://api.crossref.org/works/10.1109/icaiset66439.2026.11542036 — paper_4_crossref
    > "IoT-Based Automated Mushroom House"
[31] https://api.crossref.org/works/10.57180/ngmd7490 — paper_5_crossref
    > "Mushroom Disease Detection"
[32] https://ieeexplore.ieee.org/document/11601212 — paper1_ieee
    > "we need to verify that you're not a robot"
[33] https://thesai.org/Publications/ViewPaper?Volume=15&Issue=4&Code=IJACSA&SerialNo=54 — paper2_publisher
    > "We evaluated a dataset of 1400 images from two strains of Pleurotus ostreatus mycelium samples over a period of 14 days."
[36] https://ieeexplore.ieee.org/abstract/document/11601212 — paper1_ieee_alternative
    > "a dataset comprising healthy, green mold, black mold fruiting bags was collected from mushroom farms in Laguna."
[39] https://api.crossref.org/works/10.58532/nbennurngcdb1p1c2 — chapter2026_crossref
    > "AUTOMATING MUSHROOM CULTURE CLASSIFICATION"
[40] https://api.crossref.org/works?query=jrbx34k77g&rows=20 — exact_crossref_retry
    > "{
  "status": "ok",
  "message-type": "work-list",
  "message-version": "1.0.0",
  "message": {
    "facets": {},
    "total-results": 0,
    "items": [],
    "items-per-page": 20,
    "query": {
      "start-index": 0,
      "search-terms": "jrbx34k77g"
    }
  }
}"
