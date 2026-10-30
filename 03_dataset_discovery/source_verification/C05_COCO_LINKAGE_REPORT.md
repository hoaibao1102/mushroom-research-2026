# C05 COCO linkage report

Dataset selected: NO. Training authorized: NO. Research gap validated: NO. No split, model implementation, training or source annotation repair.

## Measured payload
COCO original7575953bytes, SHA256`58c3ca4d862883d927c495a5357d49a294d5411f0bc816fef5c0eabe72c20ea9`, matches publisherhash.129uniqueimage IDs/filenames,39796uniqueannotation IDs. All129images annotated, zero emptyimage records; zero orphanimage/category references. Requiredannotationfields present. Allimage records width615,height988. Two category IDs0and1 bothnamedmushroom; all39796instances reference1, category0unused. Do not silently merge/remap.

## Original and exported namespaces
Live RGBinventory129PNG. Annotationfolder130files:129JPGplusone COCOJSON. Every COCOfile_name exactly matches a published JPG filename. Everyimage.extra.name exactly matches oneoriginal RGBPNG;129one-to-onemetadata links, no missing/unmatchedparents. Example:`250319_cycle140_RGB_png.rf.52a865223ccf759f32e2d3e33117c645.jpg` → explicitextra.name`250319_cycle140_RGB.png`.
This is stronger than regex inference; no source rename applied. Byte/pixel equivalence and geometric alignment of PNG/JPG were NOT tested because noimagesdownloaded. Using exported JPG ascanonical supervisedinput avoids assuming equivalence to PNG; pixel QC still needed beforetraining.

## Time fields
Filename dates18/19/20/21March2025 have32/49/39/9records. Cycle ranges71–102,104–152,153–191,192–200. Cycle103absent; its cause unknown, not asserted toexplain129vs128. `date_captured` contains2026-03-13exporttimestamps (two seconds), not the2025acquisitiondate. Use explicitdate/cyclefilename semantics supported by README, notdate_captured, forfuturetimeordering. Noauthoritativebed/session/specimen IDs; uniquenessnotindependence.

## Annotation consistency
39434compressed RLE masks and362polygonannotations. Polygonbasicfinite/even/vertexchecks pass. RLEdimensions matchrecords.39432RLE passrun-sum/nonnegativechecks; two invalid RLEs and outsidebboxannotations25290/25520, bothimage82. Bboxes respectively[615,0,360,988]and[615,1,556,987] on615wideimage. These are realsourceinconsistencies, not corrected. `area` differsfromdecodedforegroundpixelcount for39434RLErecords; sourcearea appearsbbox-based, quantifyexactbboxproductmatch in statistics JSON. Do not trustsourcearea asmaskarea or silentlysubstitute it. RLEdecodingcheckedinteger/runs, not clinicalquality or imagealignment. Allmasks/personlabelsneeddeclaredpolicy before approvedbenchmark. Polygon/rastervalidationnotfullpixel QC.

## Historical vs release
39796instances across129releaseimages are not4361instances across12historicalbenchmarkimages. Historical12members, patchpolicy andsplitremainunresolved. Countscope difference is not contradiction. New129releaseprotocoldoesnotrequire historical12membership, but cannot be calledexactreproduction.
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
