# WP-05 Scientific Decision Matrix

Unknown evidence is not assigned a numerical score.

| Dimension | C03 Agaricus disease | C04 shiitake phenotype | C05 white-button RGB-D time series | C08 M18K |
|---|---|---|---|---|
| Accessibility | `FACT`: released payload audited | `FACT`: open metadata; 4.11 GB payload not audited | `FACT`: open Mendeley metadata/payload advertised | `FACT`: author download routes; payload unaudited |
| License | `FACT`: record CC BY 4.0 | `FACT`: data CC BY 4.0; separate article/code layers | `FACT`: CC BY 4.0 | `UNVERIFIED`: asset license inside archive |
| Integrity | `FACT`: 9,403 JPEGs decoded; no exact SHA groups | `UNVERIFIED`: image/label payload | `UNVERIFIED`: RGB-D/COCO payload | `UNVERIFIED`: release inventory/annotations |
| Label validity | `AUTHOR_REPORTED`; `kw` provisional; lab confirmation unknown | `AUTHOR_REPORTED`; actual boxes unaudited | `AUTHOR_REPORTED`: cap masks; no disease/maturity labels | `AUTHOR_REPORTED`: boxes/masks/pose/temporal IDs; release mapping unaudited |
| Independent sample units | `MISSING`: no specimen/session IDs | `MISSING`: no released parent/farm/session mapping | `FACT`: two beds and repeated time points; independent support limited | `UNVERIFIED`: scene/bed/sequence mappings not audited |
| Leakage/dependence | High unresolved specimen risk | Parent/augmentation overlap risk unresolved | High known temporal/bed dependence | High unresolved temporal/scene dependence |
| Baseline reproducibility | `BLOCKED`: historical split/code missing | `BLOCKED`: count and code/protocol conflicts | `BLOCKED`: runnable code and exact manifests absent | `BLOCKED`: version/count/split conflicts; model package incomplete |
| Research question | Illumination robustness is not identifiable biologically | Phenotype detection possible after lineage closure | Same-facility temporal cap segmentation/tracking is the clearest narrowed question | RGB detection possible only after license/version/group closure |
| Prior work | White-light classification and related robustness methods exist | Multiple YOLO/detector comparisons already reported | RD-GuideNet and YOLO+ByteTrack already reported | Detection/segmentation/pose/growth benchmarks already reported |
| Implementation difficulty | Medium classification; scientific grouping blocker | High: 12-class detection + lineage audit | High: RGB-D, tiling, temporal grouping; narrow RGB baseline possible | High overall; small RGB detector medium after clearance |
| Compute feasibility | Plausible but not measured | Unverified multi-detector cost | YOLO path plausible; RD-GuideNet paper reports ~29 min/mosaic | Small RGB plausible; paper used DGX-2 for full experiments |
| Small-farm applicability | Disease triage conceptually useful; species/farm transfer unverified | Shiitake grading; oyster transfer unsupported | Controlled-bed monitoring; no disease or harvest-readiness labels | Agaricus bed perception; oyster transfer unsupported |
| Remaining evidence effort | Author clarification; grouping/label closure | High: payload, labels, lineage, grouping, protocol | Moderate-high but bounded: payload manifest, grouping, support, baseline | High: license, version/count, payload, IDs, grouped split |
| Decision | `CONDITIONAL_GO` for author clarification; current primary generalization `NO_GO` | `HOLD` | `CONDITIONAL_GO` for bounded verification; `HOLD` for selection | `HOLD` |

## Interpretation

- C03 remains unresolved until the author inquiry closes specimen and label evidence.
- C05 has the strongest combination of exact identity, CC BY 4.0, exact paper linkage, and explicit temporal structure, but the same temporal structure creates dependence and limits independent units.
- C04 is cultivation-relevant and shiitake-adjacent, but its augmented-data lineage and baseline conflicts make it a larger audit burden.
- C08 is relevant to real-world mushroom perception but fails the current data-license gate and has unresolved release/version/group mappings.

No final candidate is selected. The most efficient next scientific decision is a bounded C05 payload/grouping preflight while waiting for the C03 author-response deadline—not model training.
