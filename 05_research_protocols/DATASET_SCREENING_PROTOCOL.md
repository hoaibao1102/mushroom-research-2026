# Dataset screening protocol v1

1. Open a candidate record with unique ID; preserve exact supplied URL/identifier. Start all unknowns NOT_VERIFIED.
2. Check exclusion registry first. Exact `hf55tkx489` is prohibited. Resolve name/identifier/version conflicts without importing abandoned artifacts; C02 overlap is unknown.
3. In an authorized verification package, inspect primary source identity, collectors, version history, collection context and stable access. Record URL, access date, excerpt/section, evidence tag and reviewer. WP-00 does not perform this step.
4. Verify license and research/redistribution/derived-work rights. Unknown permission blocks data acquisition/use; do not guess from platform branding.
5. Verify intended task, taxonomy, annotation protocol and independent sampling unit. Record missing metadata and potential domain/collection bias.
6. Find papers and inspect explicit dataset citations, version/collection details and available code. Classify links as NOT_VERIFIED, VERIFIED_MATCH or VERIFIED_NON_MATCH only with evidence; C01 has no confirmed exact-data paper, C02 has only a proposed one.
7. Produce G0 dossier: source identity, provenance, license/access, exclusion check, paper relationship findings and unresolved issues. Reviewer records GO/NO-GO/BLOCKED/NEEDS_MORE_EVIDENCE; do not imply GO by filling a URL.
8. Only under a separately approved download/QC package, acquire data to ignored candidate raw storage with immutable manifests and run QC protocol. No scraping/downloading in WP-00.
9. Independently score criteria after evidence exists; compare candidates fairly, including non-AI alternatives and another candidate if needed. Unknowns remain unscored.
10. Write screening/comparison report with limitations and next actions; human selection follows G0/G1 evidence and a recorded decision. Do not train from screening alone.

Required report fields: candidate/version, reviewer/date, source/evidence table, permissions, task/labels, independent units, risks/mitigations, paper relationship, rubric coverage, blockers, proposed outcome, decision ID.
