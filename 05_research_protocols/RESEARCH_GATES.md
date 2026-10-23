# Research gates v1

All gates start NEEDS_MORE_EVIDENCE. No gate has passed. WP-00 infrastructure PASS is not G0 GO.

For **each** gate: GO = entry/evidence/decision criteria satisfied with dated reviewer and decision ID; NO-GO = evidenced irreparable incompatibility or justified research stop; BLOCKED = known missing prerequisite/permission/resource prevents assessment; NEEDS_MORE_EVIDENCE = assessment possible but evidence insufficient or contradictory. Never equate unknown with failure or approval. Record outcome, reviewer, evidence paths, rationale and next action; no invented sign-off.

## G0: Dataset identity and source verified
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: Candidate record and supplied URLs; no data required.
- Required evidence: Dated primary-source identity/version/provenance/license/access record; exclusion identity/overlap check; paper-link findings.
- Decision criteria for GO: Legal intended use and exact identity established; excluded identity rejected; unverified paper link remains explicit and may block paper-dependent claims.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.

## G1: Dataset QC completed
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: G0 GO and explicit acquisition/QC authorization.
- Required evidence: Checksums, decode/label/group audits, duplicate groups, defensible split manifests, unresolved-issue log.
- Decision criteria for GO: Integrity and labels auditable; leakage controlled at independent-unit level; critical unknowns resolved or scope restricted.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.

## G2: Baseline reproducibility established
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: G0/G1 GO, reviewed selection, frozen reproduction protocol and explicit baseline training authorization.
- Required evidence: Source method/code/license, environment/config/commit, seed list, real run logs/metrics and reproduction comparison.
- Decision criteria for GO: Predeclared reproduction tolerance met or discrepancies scientifically resolved; reproducibility independently reviewed.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.

## G3: Research gap validated
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: G2 GO and structured literature/domain search; no automatic novelty assumption.
- Required evidence: Gap matrix, prior-art search log, source vs independent limitations, counterevidence, falsifiable hypothesis.
- Decision criteria for GO: Specific meaningful unresolved question supported by evidence, with feasibility and alternative/non-ML explanations considered.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.

## G4: Controlled improvement experiment completed
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: G2/G3 GO, frozen analysis plan, explicit improvement training authorization.
- Required evidence: Paired seeds/splits/budgets, ablations, all real outcomes, resource measurements, uncertainty and deviations.
- Decision criteria for GO: Controlled experiment executed and analyzed fairly; negative/null outcome allowed, no required gain.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.

## G5: Scientific conclusions and limitations reviewed
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: G4 evidence complete.
- Required evidence: Independent claim-to-evidence review, leakage/statistical audit, limitations and reproducibility dossier, paper draft.
- Decision criteria for GO: Claims match measured scope, uncertainty and failure cases; no unsupported generalization.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.

## G6: External validation readiness assessed
- Initial status: NEEDS_MORE_EVIDENCE
- Entry conditions: G5 review complete; no assumed deployment authorization.
- Required evidence: Farm consent/privacy/safety plan, isolated external test design, operational metric/budget and shift-risk assessment.
- Decision criteria for GO: Readiness or non-readiness justified; GO authorizes planning only, separate collection/deployment consent still required.
- Possible outcomes: GO, NO-GO, BLOCKED, NEEDS_MORE_EVIDENCE (definitions above apply to this gate).
- If not GO: document missing/contradictory evidence and remediation or stop decision; do not advance dependent work.
