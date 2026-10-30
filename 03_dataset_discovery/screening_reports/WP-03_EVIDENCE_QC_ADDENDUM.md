# WP-03 evidence QC addendum (WP-04 correction)

## Scope and invariants

All 202 historical records are retained in original order with their evidence and candidate IDs. The original CSV is untouched. Only the corrected registry, this addendum, and the correction subdirectory are written. No network, dataset payload, image, weight, training, commit or push operations were performed.

Historical SHA-256: `8b467a44a850bd95ba2eaeb4c575d0a1dc8a52f61b53210a5d43957765b1fb2f`.

## Code-derived counts

```json
{
  "historical_rows": 202,
  "corrected_rows": 202,
  "historical_blank_urls": 149,
  "recovered_previously_blank_urls": 149,
  "corrected_blank_urls": 0,
  "mapped_rows": 202,
  "quote_verified_rows": 202,
  "unresolved_rows": 0,
  "contradicted_rows": 6,
  "status_counts": {
    "SOURCE_FACT_VERIFIED_IN_SAVED_TEXT": 44,
    "AUTHOR_REPORTED_NOT_REPRODUCED": 143,
    "AUTHOR_PROPOSAL_NOT_VALIDATED": 9,
    "AUTHOR_REPORTED_RESULT_CONTRADICTED": 6
  },
  "candidate_counts": {
    "C03": 73,
    "C04": 49,
    "C05": 33,
    "C06": 1,
    "C07": 18,
    "C08": 28
  },
  "duplicate_semantic_claim_groups": [
    [
      "WP03-E158",
      "WP03-E173"
    ],
    [
      "WP03-E175",
      "WP03-E182"
    ],
    [
      "WP03-E176",
      "WP03-E200"
    ]
  ],
  "generic_claim_rows": 0,
  "max_excerpt_words": 35,
  "historical_sha256_before": "8b467a44a850bd95ba2eaeb4c575d0a1dc8a52f61b53210a5d43957765b1fb2f",
  "historical_sha256_after": "8b467a44a850bd95ba2eaeb4c575d0a1dc8a52f61b53210a5d43957765b1fb2f",
  "corrected_sha256": "d0abe8a26374628533214b4376a199fcea58204305245115ecdcbfc9e2e8f1e3",
  "ids_order_and_candidates_preserved": true
}
```

## Recovery and classification

Stream A: map C03–C06 to A01–A04, preserve nested evidence order, require candidate/quote/locator equality, then join the nested source_id to source_ledger.json. This recovers missing URLs without inventing them. Stream B: require exact normalized quote, locator and URL equality in claim_evidence.json, then join citation_id to citation_ledger.json. Access logs provide independent HTTP-200 cross-checks; saved originals are linked by their actual repository paths.

Every specific_claim is a manually interpreted proposition, not an ID-prefixed generic excerpt label. The script rejects generic template phrases and duplicate claims unless the original candidate/quote/locator triple is itself identical. Genuine historical duplicates remain visible rather than being fabricated into distinct claims. All original generic claims remain verbatim in original_claim.

SOURCE_FACT_VERIFIED_IN_SAVED_TEXT means a structural/document/advertised-repository fact is present, not that the underlying experiment is true. AUTHOR_REPORTED_NOT_REPRODUCED includes methods, outcomes, interpretations and secondary literature reports; AUTHOR_PROPOSAL_NOT_VALIDATED covers author future-work suggestions (not reviewer evidence). AUTHOR_REPORTED_RESULT_CONTRADICTED identifies explicit within-paper numeric conflicts. UNRESOLVED would require a blank URL when provenance or saved-text support cannot be established. No reviewer-generated performance hypothesis has been upgraded to a source result. Confidence describes document traceability only.

## Contradictions and contamination

WP03-E011 conflates ResNet-50 weighted score 99.70% with accuracy, whereas the result text gives 99.66% accuracy. WP03-E012/E015/E017/E018/E019 claim DenseNet-201 accuracy 99.98% despite 99.44% in the results/discussion. These six flags are internal consistency findings, not experimental falsifications. E056 preserves the later discussion value and cross-reference.

E080 and E081 are unrelated web-page recommendation titles. Bibliography rows are identified as citations rather than evidence of dataset use. Captions/headings establish only the content indicated, not new numeric results. SMS3D full-set author-contact restrictions and M18K differing README/paper scope remain explicit, rather than declaring every historical statement false or replacing it with one current count. C03 private-data wording and later Zenodo availability remain version/subset uncertainties, not a fabricated resolved contradiction.

## Quote verification and limitations

The full historical quotation is checked against its saved text or decoded JSON string values; matching normalizes only whitespace and HTML entities. Short supporting excerpts are contiguous spans of those checked quotations (at most 35 words). Full original quotations remain in the unchanged historical CSV. Compact quotes may not express every clause of a manually recovered proposition; consult the linked original locator and row audit. For table fragments the corrected locator includes table headers, model/backbone/task/channel context recovered from adjacent saved lines.

No new live retrieval or empirical audit was performed. An HTTP-200 log documents historical retrieval, not current availability. A source statement is not proof of correctness, leakage absence, annotation quality, license compatibility, reproducibility or real-farm transfer. Unique evidence IDs do not imply independent observations.

## Reproduction

`python 03_dataset_discovery/source_verification/wp04_evidence_correction/correct_registry.py`

Inputs: unchanged historical CSV, claims.txt, both original stream evidence/ledgers/access logs and saved text. Outputs: corrected CSV, this addendum, verification.json (per-row mappings, saved-source hashes, quote checks and counts). The script performs no network calls.
