# Day 5 dense-scene counting results

Khang compared NMS IoU 0.70 with 0.50 on eight selected crowded WB test images. The mean absolute count error fell from 3.375 to 1.875 mushrooms per image. Six images improved and two worsened.

The selection was based on ground-truth instance count and bounding-box overlap. `selected_images.csv` still records visual confirmation as pending. This is a promising pilot result, not evidence of a full-test improvement. No model retraining or 450-image re-evaluation was performed.

See `findings.md`, `comparison.csv` and `figures/` for the submitted evidence.
