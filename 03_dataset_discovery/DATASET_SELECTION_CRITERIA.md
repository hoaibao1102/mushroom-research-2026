# Dataset selection criteria — proposed rubric v1

No candidate is scored in WP-00. Unknown = NOT_VERIFIED (never a zero). These are prospective team policy thresholds, not dataset facts. Review thresholds before accessing evaluation outcomes.

## Hard exclusions vs blockers
- Confirmed exact excluded identity `hf55tkx489` or confirmed prohibited reuse of its artifacts: NO-GO. Name similarity alone is not proof; unresolved overlap is BLOCKED pending evidence.
- Confirmed lack of legal permission for intended research, irreparable provenance/integrity, no usable target labels, or unavoidable train/test leakage invalidating the question: NO-GO with evidence.
- Unknown license/access, independent units, metadata or unresolved exclusion identity: BLOCKED / NEEDS_MORE_EVIDENCE, not automatic exclusion. Do not add to exclusion registry without confirmation and a decision.
- No reproducible assessment path within declared resources: BLOCKED until scoped or NO-GO after review.

## Weighted preferences
Score 0–4 only with evidence. Common levels: 0 = verified unacceptable, 1 = weak/major documented limitations, 2 = usable with mitigation, 3 = strong/reproducible, 4 = independently validated and fully documented. Criterion-specific anchors below override generic interpretation. Values 1 and 3 require explicit evidence between neighboring anchors. Missing evidence is NOT_VERIFIED.

| Criterion | Weight | 0 anchor | 2 anchor | 4 anchor |
|---|---:|---|---|---|
| Provenance | 10 | Origin disproven/untraceable | Origin/version traceable, partial collection context | Origin, collectors, collection protocol and version independently corroborated |
| Accessibility | 5 | Confirmed unavailable legally | Stable documented access with manual steps | Public versioned retrieval reproducible from instructions |
| License | 8 | Explicit intended-use prohibition | Research permission confirmed, redistribution limits recorded | Clear reusable license, attribution/derivative obligations resolved |
| Annotation quality | 10 | Audit shows unusable targets | Defined taxonomy and audited sample with disagreements documented | Expert-reviewed protocol plus adjudication and inter-rater evidence |
| Dataset integrity | 7 | Irrecoverably corrupt | Checksummed manifest; all load failures accounted for | Complete reproducible manifest; zero unexplained integrity failures |
| Independent samples | 10 | No defensible independent test | Group IDs known, feasible test uncertainty estimate | Adequate per-group/class precision justified by prospective sample/CI analysis |
| Duplicate/leakage risk | 10 | Unavoidable contamination | Exact/near-duplicate groups controlled, residual risk explicit | Specimen/batch/time groups validated and leakage audits independently reproduced |
| Class distribution | 5 | Target class unassessable | Per-group class counts support declared metric with caveats | All target classes have justified evaluation precision and group coverage |
| Baseline reproducibility | 10 | No recoverable method or baseline | Method/config largely recoverable, missing details explicit | Code/license/config/splits/versions sufficient for independent reproduction |
| Paper relevance | 5 | No relevant scientific context | Problem/method relevant, exact data relation unresolved | Exact data/method relation verified and strong context comparison |
| Research gap evidence | 7 | Hypothesis contradicted without resolution | Specific testable question supported but incomplete | Triangulated gap, prior-art search and counterevidence reviewed |
| Computational feasibility | 5 | Confirmed exceeds declared budget | Estimated feasible with recorded assumptions | Measured/reproducible resource evidence within approved budget |
| Mushroom domain relevance | 5 | No cultivation relevance | Practitioner problem plausible, not yet broadly corroborated | Cultivation decision and benefit validated with contextual evidence |
| Real-world validation feasibility | 3 | Confirmed infeasible/unsafe | Plausible site/protocol with unresolved logistics | Consented independent site, safety and measurement protocol feasible |

Weights sum to 100. Weighted total = sum(weight × score / 4), out of 100, only when all required evidence is available; otherwise report coverage and observed subtotal, never renormalize unknowns to make a candidate win. Also report raw criterion scores, evidence and uncertainty. No universal sample-count or accuracy threshold is fabricated: specify required precision and resource budget before scoring.

## Selection procedure
Two reviewers independently score evidence, reconcile disagreements, record counterevidence and hard blockers, and write a signed decision comparing C01, C02 and any additional candidates. Proposed recommendation threshold: at least 70/100, no hard exclusions, no unresolved critical blockers, G0/G1 GO; threshold is policy, not a result. Below threshold: gather evidence, narrow scope, add candidates or NO-GO. Baseline reproducibility/gap scores reflect available evidence, not a claim that G2/G3 have passed. Final selection requires an explicit decision, not the highest score alone.
