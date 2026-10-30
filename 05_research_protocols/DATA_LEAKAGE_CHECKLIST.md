# Data leakage checklist — V2 status

- [x] Dataset's provided train/valid/test folders identified (3,596 / 449 / 450).
- [x] Exact filename overlap checked: 0 matches reported in completed notebook. **This does not establish independence.**
- [ ] SHA-256 hash of image content across splits.
- [ ] Perceptual/near-duplicate grouping, including repeated cultivation trays and time series.
- [ ] Confirm crops/augmentations of the same source remain within one split.
- [ ] Inspect available capture IDs, batch and time metadata; define independent unit.
- [ ] Determine whether original V2 80/10/10 split is appropriate to the claimed generalization setting.
- [ ] Freeze split manifest plus version/hash before model comparisons.
- [ ] Check pretraining overlap and only tune/choose checkpoints on validation.
- [ ] Keep test split sealed until final evaluation.
- [ ] Review remaining risks and sign off with dated evidence.

The completed notebook only supports the first two checked items. **Scene-level independence and full duplicate safety are unverified.**
