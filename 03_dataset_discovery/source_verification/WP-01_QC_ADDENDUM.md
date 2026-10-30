# WP-01 QC addendum — WP-02 pre-selection audit

This addendum corrects interpretation without rewriting original WP-01 reports or deleting original evidence. Acquisition/annotation results are recorded separately in the WP-02 candidate reports; this document does not pre-judge their outcomes.

## 1. Annotation-source oversight

The pinned WP-01 model-repository tree and README already identify author-designated COCO files:

- `MushR_Dataset_V1.1_2023_04_04-COCO.json` (training)
- `MushR_Dataset_2023_06_29_TEST-COCO.json` (testing)

Source: `https://github.com/ETCE-LAB/mushr-mask-r-cnn`; preserved evidence: `wp01_c02_code_evidence/mushr-mask-r-cnn/text/README.md` and `tree.json`, commit `e8a0493b193c15c5f6129d89d7f14d89e84a8868`. The earlier claim that Kaggle lists no JSON describes only that platform's listing. It does **not** establish annotation unavailability across author sources. WP-02 must retrieve and audit these files before deciding usability; mere file presence does not establish valid schema, compatible images or reproducibility.

## 2. Dataset identity overstatement

Superseding conclusion: **PROVENANCE_DISTINCT_IMAGE_OVERLAP_NOT_TESTED**.

WP-01 describes different author/institution/collection provenance for MushR and excluded DS-02. It did not perform image-level comparison. Thus phrases such as “zero risk”, “zero shared data” or unqualified image independence are unsupported. No DS-02 asset acquisition is authorized; its exclusion remains in force. This correction qualifies WP-01 evidence rows `CLM-DS02-03` and `CLM-DS02-04` and the identity report; original rows remain historical, not authoritative proof of pixel independence.

## 3. Literature-search bounds

Use **NO_EXACT_DATASET_PAPER_CONFIRMED** for C01. WP-01's bounded searches do not prove that no paper or benchmark exists. The categorical wording in the top-level source report, comparison and feasibility report exceeds the narrower original claim `WP01-020`. Same-task work on different datasets is not confirmed reuse of C01. No novelty or research gap follows from a missing search result.

## 4. Compute, biology and leakage uncertainty

WP-01 training-time, VRAM, checkpoint-size and cross-platform runtime forecasts were engineering estimates, not measured benchmarks. Treat those numbers as **UNVERIFIED**; no training occurred. Published MushR hardware/resource figures are author reports, not local measurements.

Missing bag IDs motivate dependence checks; they do not prove repeated specimens or guarantee leakage. Lack of a documented laboratory protocol does not prove that laboratory confirmation never occurred. Likewise, broad farm-loss, humidity, spore-production and deployment claims in synthesized feasibility documents were not individually supported by an adequate evidence chain and must not be treated as verified domain facts. Field benefit and non-ML alternatives require independent domain validation.

## 5. Git-history inconsistency

The historical WP-01 report incorrectly described its newly generated, then-uncommitted working tree as clean. Subsequent checkpoint commit `da1688a56c51ace38b77ee5dfb6323277bac7843` now preserves the reports and source evidence. WP-02 pre-flight confirmed branch `research/wp-02-feasibility-audit`, clean working tree and HEAD `f50f946b1d5f1bd11407c09b3b210ae0370fbde2` (temporary-directory fix). `git ls-files` lists WP-01 reports/evidence registry; `git check-ignore -v` on the report and registry returned no matching rule (exit 1, expected for retained files). Pre-flight validator: 38 PASS / 0 FAIL; tests: 9/9 passed. This present safety observation does not retroactively validate the historical clean-tree claim.

## 6. Gate and review scope

Source accessibility, annotation structural integrity, image–label linkage, biological truth, independent evaluation, baseline reproduction and research novelty are separate checks. G0 identity assessment must not be conflated with G1 full QC or G2 execution. WP-02's explicitly authorized acquisition is a limited pre-selection audit, not an assertion that earlier gates passed. No final candidate selection, automatic class repair, training or research-gap confirmation is authorized. Original scientific gates remain pending human review.
