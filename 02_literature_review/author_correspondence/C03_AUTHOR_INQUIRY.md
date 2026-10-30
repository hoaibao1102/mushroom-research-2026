# C03 author inquiry — DRAFT_NOT_SENT

Verified correspondence address: **ugur.coruh@erdogan.edu.tr**. Source [P], XML `author-notes/corresp[@id="c1-agronomy-15-00226"]/email`. The draft does not claim mailbox deliverability. Other author addresses are not needed. Source XML SHA256:d5335af7db63c6b072485b56f65cb68859e8555ba2de756fff7907f456fdfe87. Live recheck403, contact verified from preserved primary fulltext.

## Email draft (manual sending only)
To: ugur.coruh@erdogan.edu.tr
Subject: Request for specimen and acquisition metadata for the Agaricus disease image dataset

Dear Corresponding Author,

We are preparing a university Software Engineering capstone feasibility study using the public dataset at https://zenodo.org/records/20260929 and your paper “Classification and Analysis of Agaricus bisporus Diseases with Pre-Trained Deep Learning Models” (DOI:10.3390/agronomy15010226). We have not trained models or selected a final research topic. We would appreciate clarification to design a scientifically defensible evaluation:

1. Do White, UV and Mixed folders include repeated photographs or different views of the same biological mushroom specimens, within or across illumination conditions?
2. Are original specimen IDs or image-to-specimen mappings available? If IDs were not recorded, is there an authoritative acquisition log or other defensible grouping record?
3. Can image-level collection session, farm, date or cultivation-batch metadata be shared, including how each field was defined?
4. Are the original training/validation file manifests, random seeds and preprocessing details for the 2025 paper available?
5. Does the folder named `kw` represent Cobweb disease? Could you confirm the full folder-to-disease mapping and how uncertain or mixed diagnoses were handled?
6. Are the released 3,195 white-light images exactly the samples used in the 2025 paper, or were any images renamed, recropped, reprocessed, added or removed?
7. Were diagnosis labels established by expert visual assessment, laboratory confirmation, or both? Are diagnostic criteria and any image-level confirmation records available?

An anonymized mapping (for example filename, opaque original specimen ID, session/batch ID, illumination and label provenance) would be sufficient. We do not need sensitive farm names, addresses or personal information. Please let us know whether non-sensitive metadata can be shared and under what use conditions. If a field was never recorded, knowing that would also help us avoid unsupported independence claims.

Our feasibility decision target is 6 November 2026. We understand if a response is not possible by then. We will not interpret a lack of response as rejection or as evidence about the collection procedure.

Thank you for your time and for making the dataset available.

Best regards,
[Sender name]
[University / capstone team]
[Institutional email]

## Sending status
NOT_SENT; sender details intentionally left for the human sender. No response received or fabricated; author has not yet been contacted by this workflow. No background monitoring is scheduled.

Training authorized: NO. Dataset selected: NO. Research gap validated: NO. No gate promotion. Decision preparation:2026-10-30; deadline:2026-11-06.
## Source ledger / evidence boundaries
- [P] Primary paper DOI https://doi.org/10.3390/agronomy15010226 ; publisher https://www.mdpi.com/2073-4395/15/1/226 ; full XML https://mdpi-res.com/d_attachment/agronomy/agronomy-15-00226/article_deploy/agronomy-15-00226.xml . Local original: `03_dataset_discovery/source_verification/wp03_stream_a/paper_xml_alternate.txt`. Locators: front/article-meta/author-notes/corresp (contact); Materials and Methods (white-light sample counts, labels, train/validation), Results/Discussion (reported models/limitations). Full text was previously acquired, not reconstructed. Both XML endpoints returned HTTP403 on2026-10-30 retry; this does not erase saved evidence or prove current accessibility.
- [Z] Primary dataset https://zenodo.org/records/20260929 ; DOI10.5281/zenodo.20260929; record identity/license/files documented in `03_dataset_discovery/source_verification/C03_DEEP_SOURCE_VERIFICATION.md`; measured source inventory `04_dataset_candidates/C03_agaricus_disease/qc/image_inventory.csv`.
- [B] Project audit, NOT primary scientific literature: `03_dataset_discovery/source_verification/C03_SPECIMEN_GROUPING_AUDIT.md`, `C03_LABEL_SEMANTICS_AUDIT.md`; `05_research_protocols/C03_PROPOSED_EVALUATION_PROTOCOL.md`; bounded120pairreview in candidate-local`qc/wp04b_readiness/bounded_similarity_review.csv`. AI assessments, no human adjudication.
- [L] Bounded prior-literature review: `02_literature_review/research_gap_analysis/C03_GAP_PRESCREEN.md` and candidate-local`qc/wp04b_readiness/literature_registry.csv`. Original dataset article https://doi.org/10.30708/mantar.1452976 (abstract scope); color-space study https://doi.org/10.3897/ejfa.2026.169921 (abstract/XML scope). No unrestricted search in WP04C; these metadata/abstract leads do not establish unseen-specimen evaluation or absence of prior work.
