# Data leakage checklist

Not executed; every box remains unchecked. Each item needs method, evidence path, reviewer and resolution.

- [ ] Exact duplicates: hash every file; duplicate groups cannot cross splits.
- [ ] Near duplicates: calibrate similarity threshold; manually review border cases and group confirmed matches.
- [ ] Augmented image leakage: trace derivatives to originals; split first, augment train only.
- [ ] Images from the same original frame: group crops, video frames and alternate exports.
- [ ] Same biological specimen across splits: identify bag/specimen; enforce grouped partition.
- [ ] Same cultivation batch across splits: separate batches where required by generalization question.
- [ ] Temporal leakage: do not use future observations/labels/features to predict past states; define chronology.
- [ ] Test-set contamination: never tune models, thresholds, preprocessing or gap hypotheses on test outcomes.
- [ ] Train-only preprocessing: normalization/feature fitting/selection use train only.
- [ ] Pretraining/source overlap: document pretrained data overlap risk before later weight use.
- [ ] External test isolation: farm images cannot enter train/validation or model selection.
- [ ] Missing group metadata: acknowledge inability to establish independence; block gate or redesign claim.
- [ ] Freeze split manifests with hashes; independently review and record residual uncertainty.

Unknown is not PASS. Any post-freeze split change requires versioned justification and reevaluation of all dependent experiments.
