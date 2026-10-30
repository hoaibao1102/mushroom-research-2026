# C05 final capstone decision

Dataset selected: NO. Training authorized: NO. Research gap validated: NO. No split, model implementation, training or source annotation repair.

## Recommendation: GO_FOR_PROTOCOL_DESIGN
This permits documented protocol design only, not datasetselection, training or scientificgapacceptance.

### A. Historical12-image YOLObenchmark
Exactreproduction NOT_ESTABLISHED: twelveparentidentities, originaltrain/testpatchmanifests, modelscale, environment/seeds andcheckpointidentity unresolved [M]. Newpublicreleasecoverage doesnotrecoverthese. Missingoriginalsplitblocks A, not automatically B.

### B. Newpublicrelease RGBsegmentationexperiment
A defensiblenarrowtarget is **forward-time prediction of visiblecap masks on later observations of the samefacility and ongoingcultivationsequence**, allowing repeatedmushrooms aspartofthetarget.129mosaics and explicitextra.nameparentlinks plusdate/cyclekeys nowallowprotocolplanning. This is notnew-specimen,farm,independentbed ornewgrowthcyclegeneralization. Dependenceacrosstimeis intrinsic, not magicallyremoved bychronology.

Protocolrequirements: parentmosaicgroupingbeforepatching; nofutureframes/labels inpreprocessing/tuning; predeclaredchronologicaltrain/development/testwindows andtemporalbuffer sensitivity; no randompatch/instance split; explicitly reportunknownbed IDs andlimited4dayonefacilityscope; aggregatemetrics bytimeblock/parent, donottreat39796objects asindependentsamples. Enoughvalidation/testtimeblocks/classsupport andwindowfeasibilitymustbe checked duringdesign withoutcreatingasplitinthisaudit. Original PNG/JPGpixelgeometrypending; prefercanonicalexported JPGnamespace unlessverified.

A source-annotation acceptancepolicy mustaddressinvalid RLE/outsidebbox IDs25290/25520andarea semantics, withreviewedversionedchanges ordeclaredexclusions beforetraining. Do notsilentlyrepair/quarantineordroprecords now. These arebounded QCtasks, notfundamentallyunrecoverablelinkage. Ifpolicy cannotretainadequatetimecoverage/reliablelabels, stopratherthantrain.

## Manageability / novelty
RGB-onlyonepopulatedclass,129mosaics, standardsegmentationbaseline andboundedparent-awarepatching ismoderatecapstonescope. Limited GPUfeasibility is engineeringestimate, notmeasuredruntime; use smallbaseline/lockedinputbudget inprotocoldesign, avoidcustom RDGuide Net/depthtracking orcustomloss. No GPUbenchmarkperformed. Temporalcapsegmentationalreadyexists; novelcontribution NOT_VERIFIED. Protocolmustdefineavaluablequestion(e.g.temporalboundaryreliability) andevidence-backedcontributionbeforefinalapproval. Architecturalswapaloneisnotnovelty.

## Stop boundary
No additionalunrestrictedmetadataauditrecommended. Next: humanreviewofthispayload QC, thenseparatelyauthorizedboundedprotocoldesign includingannotationacceptance/resourceplan. Historical129vs128causeand12memberidentitiesremainopenbutnotmandatoryfornewreleaseexperiment. No currenttrainingauthorization.
## Sources and traceability
- [D] Data paper DOI https://doi.org/10.1016/j.dib.2026.113085 ; official full text https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13452286/full Text XML . Section3 “Data Description”, Table1 and annotation discussion; acquisition methods. Fulltext read, exact evidence below.
- [R] Dataset https://data.mendeley.com/datasets/8n6nr43gk3/1 ; downloaded README, live Annotation/RGB file inventories and exact COCO original. Full URLs, sizes and SHA256 in candidate-local `qc/annotation_payload_audit/acquisition_manifest.json`; originals retained unchanged under ignored `source/payload_audit_originals/`.
- [M] Method paper https://doi.org/10.3390/s26061935 ; Section2.4 and previous project `C05_SUBSET_RECONCILIATION.md` preserve historical12mosaic benchmark/patch/4361instance scope. Historical claim not independently reproduced here.
- [Q] New empirical audit: `04_dataset_candidates/C05_white_button_rgbd/qc/annotation_payload_audit/statistics.json`, `image_linkage.csv`, and two standard-library QC scripts. File-level metadata linkage is not pixel equivalence or biological independence.
