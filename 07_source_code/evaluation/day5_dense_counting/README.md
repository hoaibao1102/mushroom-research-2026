# Dense-scene counting experiment

This script compares the existing WB-only checkpoint at two NMS IoU thresholds on eight selected crowded test images. It keeps the model, confidence threshold, image size and images the same; only NMS IoU changes (0.70 versus 0.50).

Run it in Colab after mounting Google Drive and making the existing checkpoint, test RGB images, COCO annotations and WB-only `data.yaml` available. The script writes its CSVs and figures under `M18K_Reproduction/Day5_Dense_Counting/`.

The eight images were selected using instance count and bounding-box overlap. The selection CSV still marks visual confirmation as pending, so treat the result as a small exploratory comparison, not a full-test improvement claim.
