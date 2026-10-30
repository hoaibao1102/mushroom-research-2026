# Provenance checklist for team reviewer

- [ ] Confirm archive's download URL/version/date and save SHA-256 checksum.
- [ ] Review V2 dataset image/label license separately from the paper's article license.
- [ ] Determine whether `M18KV2.tar.zst` includes unlabeled or additional images beyond the 4,495 COCO records.
- [ ] Confirm train/valid/test files are exactly the official source splits.
- [ ] Record camera intrinsics, depth units and alignment evidence if available.
- [ ] Save repository commit/version for upstream code used by the experiment.

Do not fill these automatically from assumptions; source confirmation and reviewer identity are required.
