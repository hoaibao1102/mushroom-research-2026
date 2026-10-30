# Decision log

| ID | Date | Decision | Basis | Scientific consequence | Owner |
|---|---|---|---|---|---|
| D000 | 2026-10-23 | Initialize fresh WP-00 workspace only | User WP-00 specification | No selection or verified scientific claims | User-requested scope |
| D001 | 2026-10-23 | Exclude hf55tkx489 / Annotated Oyster Mushroom Images | User explicitly abandoned DS-02 | No import/reuse; C02 identity remains unverified | User-requested exclusion |
| D002 | 2026-10-23 | Execute WP-01 candidate source verification without data downloads or model training | WP-01 specification | Public metadata, full-text paper, and author code audited statically | Research Analyst / Auditor |
| D003 | 2026-10-23 | Confirm C02 is distinct from abandoned DS-02 | Independent provenance: Germany vs Turkey, different authors, different apparatus | Eliminates contamination risk from DS-02; does not imply C02 selection | Research Analyst / Auditor |
| D004 | 2026-10-23 | Recommend G0 = NEEDS_MORE_EVIDENCE for both C01 and C02 | Missing biological truth/bag IDs (C01) and missing Kaggle annotation JSON/class mismatches (C02) | Dataset selection remains open; training strictly unauthorized | Research Analyst / Auditor |

## WP-03 initialization

2026-10-30T11:46:00.503643+07:00: User authorized new-candidate discovery after WP02 checkpoint. Remote ref d0ddfe8f4cfad0da431fc0f777a8db2163a62c2c verified using explicit manager helper. C01 HOLD; C02 NO-GO_CURRENT_HOLDOUT_SPLIT only. No final selection, validated gap or training permission. Earlier decision rows preserved as historical evidence, qualified by WP01 QC addendum.
