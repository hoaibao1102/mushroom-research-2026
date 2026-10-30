# C05 final annotation payload audit
Date:2026-10-30

Dataset selected: NO. Training authorized: NO. Research gap validated: NO. No split, model implementation, training or source annotation repair.

## Git preservation
WP05alreadycommittedatc318519d6c446e838d55e55424928e8c8209fbc5; saved WP05receipt PASS. Threeprevious C05preflightreportsreviewedandcommittedas9be4cfb (docs(research): preserve C05 metadata preflight), no rawdata/sourcecopiesstaged. Compatible5rejectiontestspassed, exit0. First60secondtestrun timedout; reruncompleted186.155seconds. No forcepush/reset/merge. Userdidnotrequirepush; localcheckpointonly, currentbranchresearch/wp-05-candidate-decision. Newauditoutputs NOTcommitted.

## Controlled access / new evidence
Direct JSONdownload HTTP200,7575953bytes, publisher SHA256matched. Noarchive/full RGB/depth/image/weightsdownloads. Preservedannotationandsupportfiles total7954983bytes; page/bundle/search/duplicatemetadatarequests stillwellbelow100MBcumulative. Browserblockedbyprofilelock, urllib403; curlread-onlypublicendpointsworked. APIroutesderivedfromactualfrontendbundle, notunrelatedsearchresponses. Originalmetadataunchangedandignoredusinglocal.git/info/exclude; verifygitcheckignorebeforehandoff.

Read data-descriptionpaper Section3/Table1/annotationdiscussionfromofficial PMCfulltext. Confirms sourceexplicitlyreportsall129COCOannotations and Roboflow JPGnamespace, correctingthepreviousmetadataonlyuncertaintywithoutrewritinghistory.

## Measured results and decision
129unique COCOimages,39796instances,129annotated,0empty,0orphanreferences.129RGBPNGmetadatarecords,129export JPGmetadatarecords,all129extra.namematch PNG. Onepopulatedcategory ID1; unusedcategory0samehumanname.39434RLE/362polygonrecords. Twoinvalid RLE/outsidebboxannotationsinimage82; area semanticsnotmaskarea. date_capturedisexporttime, filenameacquisitiondate/cyclemustbeused. See detailedlinkagereport/statistics forcounts,examplesandunresolvedpixelgeometry.

GO_FOR_PROTOCOL_DESIGN fornewdocumentedsamefacilitytime-aware RGBsegmentation only; historical12imageexactreproductionstillblocked. Thisnarrowsclaim, doesnotclaimbiologicalindependenceornewfarmgeneralization. No noveltystatusupgrade.

## Verification
QCscriptstworuns completedexit0; exact JSONSHAchecked; links/counts/RLEdecoded. Machine-readable statistics,129rowlinkage CSV, acquisitionmanifest and C05_PAYLOAD_VALIDATION.json recordactualchecks/hashsnapshot. Tests5/5PASS; gitdiffcheckpass. Fullimage/polygonraster QC, clinicalmaskquality and GPUtime NOT_VERIFIED. No training/split/modelimplementation/selection/gatepromotion/DS02access.
## Exact source evidence (short excerpts)
[D], Section3 Table1, Annotation/ row: “Pixel-level mushroom cap annotations for all 129 RGB images”.
[D], annotation discussion: “The exported annotation folder also contains Roboflow-generated JPG image files with unique filename identifiers.”
[R], README: “File naming convention: YYMMDD_cycle XX_Type.extension”.
[D] further states that dates and cycle numbers match original RGB/depth mosaics. These are source claims; payload coverage and keys were independently inspected below.
## Sources and traceability
- [D] Data paper DOI https://doi.org/10.1016/j.dib.2026.113085 ; official full text https://www.ebi.ac.uk/europepmc/webservices/rest/PMC13452286/full Text XML . Section3 “Data Description”, Table1 and annotation discussion; acquisition methods. Fulltext read, exact evidence below.
- [R] Dataset https://data.mendeley.com/datasets/8n6nr43gk3/1 ; downloaded README, live Annotation/RGB file inventories and exact COCO original. Full URLs, sizes and SHA256 in candidate-local `qc/annotation_payload_audit/acquisition_manifest.json`; originals retained unchanged under ignored `source/payload_audit_originals/`.
- [M] Method paper https://doi.org/10.3390/s26061935 ; Section2.4 and previous project `C05_SUBSET_RECONCILIATION.md` preserve historical12mosaic benchmark/patch/4361instance scope. Historical claim not independently reproduced here.
- [Q] New empirical audit: `04_dataset_candidates/C05_white_button_rgbd/qc/annotation_payload_audit/statistics.json`, `image_linkage.csv`, and two standard-library QC scripts. File-level metadata linkage is not pixel equivalence or biological independence.
