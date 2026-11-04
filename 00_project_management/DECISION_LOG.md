# Decision log

| ID | Date | Decision | Basis | Scientific consequence | Owner |
|---|---|---|---|---|---|
| D000 | 2026-10-23 | Initialize fresh WP-00 workspace only | User WP-00 specification | No selection or verified scientific claims | User-requested scope |
| D001 | 2026-10-23 | Exclude hf55tkx489 / Annotated Oyster Mushroom Images | User explicitly abandoned DS-02 | No import/reuse; C02 identity remains unverified | User-requested exclusion |

Future template: decision ID, timestamp, owner/reviewer, alternatives, evidence paths, uncertainty, outcome, affected state/protocol version, reversal conditions. Do not invent team approvals.
| D002 | 2026-10-30 | Use M18K V2 as the **provisional working dataset** for Team 10 integration | User-directed research focus in this conversation; executed V2 notebook | Add C03 and recorded EDA; **not** a team-lead selection or G0/G1 approval | Project preparation (approval pending) |
| D003 | 2026-10-30 | Do not claim model reproduction from today's work | Uploaded completed notebook has `RUN_TRAIN=False`; no held-out scores | EDA-only record; model experiments remain planned | Evidence-based status update |

Future project decisions require reviewer, rationale, evidence location and team approval where appropriate.

| D004 | 2026-11-02 | Record two-class and WB-only YOLOv8n-seg results as Day 2 reproduction of the **approach on V2** | Completed user-supplied training/test evidence | Do not claim original numerical benchmark matched or exceeded | Research lead/user workflow; formal gate approval not inferred |
| D005 | 2026-11-03 | Record 30-image area and 12-image qualitative findings as Day 3 additional analysis | Submitted notebooks, CSVs, figures and reviewed report | px² only, sample-level errors only; leave raw annotation and leakage verification open | Research lead/user workflow; formal gate approval not inferred |

| D006 | 2026-11-04 | Deliver an IVP **MVP** using the existing WB-only model, full-test area measurement, scratch Otsu, and simple ablations rather than retraining | Course rubric and executed Day 4 notebooks | Course-report and demo evidence are additional to the research reproduction; leave slides/video as pending | Research lead/user workflow; no formal gate approval implied |
| D007 | 2026-11-04 | Preserve submitted Day 4 QC but keep earlier original dHash-pair and anomaly flags unresolved | Day 4 submitted QC CSV compared different pairs and one file hash missing | Do not claim leak-free test data or entirely verified annotations | Integration review; independent data audit still pending |
