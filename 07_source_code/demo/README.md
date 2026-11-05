# WB-only Gradio demo

This small app runs the existing WB-only YOLOv8n-seg checkpoint on an RGB image. It can load a random image from the M18K V2 test split or accept an uploaded image. It displays the predicted instance masks and count, and exports an annotated image, an instance-ID mask, and CSV measurements.

## Run in Colab

Open `08_experiments/notebooks/Day5_WB_Only_Gradio_Demo.ipynb` and run the cells. The notebook mounts Drive, sets the test-image folder, downloads the existing checkpoint, installs the demo dependencies and starts Gradio with a temporary share link.

The default test-image folder is `/content/drive/MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/test/rgb`. The checkpoint is the existing WB-only `best.pt` shared by the team.

The app reports predicted counts and projected mask areas in px². These are not ground-truth measurements or physical areas in mm². The user confirmed that the Colab demo launched and the random-image workflow worked on 5 November 2026.
