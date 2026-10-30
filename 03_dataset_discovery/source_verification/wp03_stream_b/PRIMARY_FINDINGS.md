# WP03 stream B: primary-source findings

Three plausible cultivated-mushroom dataset-paper pairs were identified; all remain conditional, not selected.

- B01 SMS3D: paper reports40,000 synthetic scenes; live author README requires contact for full40K and offers2,000 scenes per type. Missing scan/soil assets and dataset-rights verification block unconditional reuse.[1][2]
- B02 M18K: paper reports2,000 main RGB-D images plus3,838 growth images; live README V2 advertises4,652 segmentation images and2,121 growth images. Version/count reconciliation is mandatory; no archives inspected.[3][4]
- B03 Dutt/Choi/Pecchia RGB-D v1: exact DOI8n6nr43gk3.1 directly linked by both data article and RD-GuideNet. This is fixed-view temporal cap segmentation, not verified maturity classification. The authors explicitly limit camera/facility/variety coverage.[5][6][7]

## Research-direction controls

H01: simple SMS3D-to-M18K pretraining is already addressed in SMS3D Table5. H02: depth-guided segmentation plus tracking is already addressed in RD-GuideNet2026. A broader novelty claim is unsupported by this bounded search; see candidates.json hypotheses and saved search responses. These are reviewer assessments, not author claims of novelty.

## Access and boundaries

No full datasets, standalone images, weights, model fitting, or training were downloaded or run. Publisher article PDFs contain publication figures but no dataset archives were fetched. Code review is metadata/tree/README/license only. Dataset license remains unresolved for B01/B02 despite permissive code licenses. No shared registries or state files were changed.

## Sources

[1] https://mdpi-res.com/d_attachment/computers/computers-14-00128/article_deploy/computers-14-00128.pdf — SMS3D publisher full text
[2] https://github.com/abdollahzakeri/sms3d — SMS3D author repository
[3] https://mdpi-res.com/d_attachment/computers/computers-14-00199/article_deploy/computers-14-00199.pdf — M18K publisher full text
[4] https://github.com/abdollahzakeri/m18k — M18K author repository
[5] https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13452286/fullTextXML — Dutt Choi data article full text
[6] https://data.mendeley.com/datasets/8n6nr43gk3/1 — Mendeley RGB-D v1 metadata
[7] https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13030075/fullTextXML — RD-GuideNet full text
