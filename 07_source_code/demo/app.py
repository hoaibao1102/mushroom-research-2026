"""M18K V2 White Button mushroom inference demo (Gradio)."""
from __future__ import annotations

import os
import random
import tempfile
from pathlib import Path
from typing import Any

import cv2
import gdown
import gradio as gr
import numpy as np
import pandas as pd
import torch
from ultralytics import YOLO

MODEL_FILE_ID = os.getenv("M18K_MODEL_FILE_ID", "1Q5iq_-j-RwOTkyiiXyTOc80Cf_xwk7K-")
MODEL_PATH = Path(os.getenv("M18K_MODEL_PATH", "/content/khang_wb_best.pt"))
TEST_RGB_DIR = Path(os.getenv(
    "M18K_TEST_RGB_DIR",
    "/content/drive/MyDrive/M18K_Reproduction/M18K_V2_data/M18KV2/test/rgb",
))
IMAGE_SIZE = int(os.getenv("M18K_IMAGE_SIZE", "640"))
MAX_DETECTIONS = int(os.getenv("M18K_MAX_DETECTIONS", "1000"))
MASK_ALPHA = 0.40
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def load_model() -> YOLO:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not MODEL_PATH.is_file():
        print("Downloading WB-only checkpoint from Google Drive...")
        downloaded = gdown.download(id=MODEL_FILE_ID, output=str(MODEL_PATH), quiet=False)
        if downloaded is None or not MODEL_PATH.is_file():
            raise FileNotFoundError(
                "Checkpoint download failed. Set M18K_MODEL_PATH to a local best.pt path "
                "or check that the Google Drive file is accessible."
            )
    model = YOLO(str(MODEL_PATH))
    names = model.names
    if len(names) != 1 or str(names.get(0, "")).strip().lower() not in {
        "wb", "white button", "white_button"
    }:
        raise ValueError(f"Expected a one-class WB checkpoint; got model.names={names}")
    print(f"Loaded checkpoint: {MODEL_PATH}")
    print(f"Device: {'CUDA:0' if torch.cuda.is_available() else 'CPU'}")
    return model


MODEL = load_model()
DEVICE: int | str = 0 if torch.cuda.is_available() else "cpu"


def load_random_test_image() -> tuple[np.ndarray, str]:
    """Load one random RGB image from the existing M18K V2 test/rgb folder."""
    if not TEST_RGB_DIR.is_dir():
        raise gr.Error(
            f"Test RGB folder not found: {TEST_RGB_DIR}. Mount Google Drive in Colab "
            "or set M18K_TEST_RGB_DIR to the correct test/rgb path."
        )
    paths = sorted(
        p for p in TEST_RGB_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not paths:
        raise gr.Error(f"No supported images found in {TEST_RGB_DIR}")
    selected = random.choice(paths)
    bgr = cv2.imread(str(selected), cv2.IMREAD_COLOR)
    if bgr is None:
        raise gr.Error(f"Could not read selected image: {selected.name}")
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb, selected.name


def _instance_color(index: int) -> tuple[int, int, int]:
    # Stable RGB colors; adjacent instances receive visibly different colors.
    return (
        int(50 + (index * 97) % 190),
        int(45 + (index * 61) % 190),
        int(45 + (index * 131) % 190),
    )


def analyze_image(
    image_rgb: np.ndarray | None,
    confidence: float,
    nms_iou: float,
    draw_boxes: bool,
) -> tuple[Any, str, pd.DataFrame, str | None, str | None, str | None, str | None]:
    if image_rgb is None:
        raise gr.Error("Choose an image or load a random M18K V2 test image first.")
    if image_rgb.ndim != 3 or image_rgb.shape[2] != 3:
        raise gr.Error("Input must be a 3-channel RGB image.")

    image_rgb = np.ascontiguousarray(image_rgb.astype(np.uint8))
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    h, w = image_bgr.shape[:2]

    result = MODEL.predict(
        source=image_bgr,
        imgsz=IMAGE_SIZE,
        conf=float(confidence),
        iou=float(nms_iou),
        max_det=MAX_DETECTIONS,
        retina_masks=True,
        device=DEVICE,
        verbose=False,
    )[0]

    boxes = result.boxes
    masks_obj = result.masks
    count = 0 if boxes is None else len(boxes)
    if masks_obj is None:
        masks: list[np.ndarray] = []
    else:
        raw_masks = masks_obj.data.detach().cpu().numpy()
        masks = []
        for raw in raw_masks:
            if raw.shape != (h, w):
                raw = cv2.resize(raw, (w, h), interpolation=cv2.INTER_NEAREST)
            masks.append(raw > 0.5)
    if count != len(masks):
        raise gr.Error(
            f"Prediction output mismatch: {count} boxes but {len(masks)} masks. "
            "Please check the installed Ultralytics version."
        )

    overlay = image_rgb.copy()
    mask_id = np.zeros((h, w), dtype=np.uint16)
    rows: list[dict[str, Any]] = []

    for i, mask in enumerate(masks):
        color = _instance_color(i)
        overlay[mask] = (
            MASK_ALPHA * np.asarray(color, dtype=np.float32)
            + (1.0 - MASK_ALPHA) * overlay[mask].astype(np.float32)
        ).astype(np.uint8)
        mask_id[mask] = i + 1

        confidence_value = float(boxes.conf[i].item())
        xyxy = boxes.xyxy[i].detach().cpu().numpy().astype(float).tolist()
        x1, y1, x2, y2 = xyxy
        rows.append({
            "instance_id": i + 1,
            "class": "WB",
            "confidence": round(confidence_value, 5),
            "mask_area_px2": int(np.count_nonzero(mask)),
            "bbox_x1": round(x1, 2),
            "bbox_y1": round(y1, 2),
            "bbox_x2": round(x2, 2),
            "bbox_y2": round(y2, 2),
        })

        # Draw mask contours for readability.
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # OpenCV draws on RGB arrays here, so reverse the BGR-style tuple.
        cv2.drawContours(overlay, contours, -1, color, thickness=1)
        if draw_boxes:
            cv2.rectangle(
                overlay,
                (max(0, int(round(x1))), max(0, int(round(y1)))),
                (min(w - 1, int(round(x2))), min(h - 1, int(round(y2)))),
                color,
                thickness=2,
            )

    columns = [
        "instance_id", "class", "confidence", "mask_area_px2",
        "bbox_x1", "bbox_y1", "bbox_x2", "bbox_y2",
    ]
    per_instance = pd.DataFrame(rows, columns=columns)
    total_mask_area = int(per_instance["mask_area_px2"].sum()) if count else 0
    mean_area = float(per_instance["mask_area_px2"].mean()) if count else 0.0
    summary = (
        f"### WB-only inference result\n"
        f"- **Detected mushrooms:** {count}\n"
        f"- **Image size:** {w} × {h} pixels\n"
        f"- **Total instance-mask area (sum):** {total_mask_area:,} px²\n"
        f"- **Mean instance-mask area:** {mean_area:,.1f} px²\n"
        f"- **Confidence threshold:** {confidence:.2f} · **NMS IoU:** {nms_iou:.2f}\n\n"
        "*Areas are per-instance projected image areas in px², not physical area in mm². "
        "Counts and areas are predictions, not ground-truth measurements.*"
    )

    output_dir = Path(tempfile.mkdtemp(prefix="m18k_wb_demo_"))
    annotated_path = output_dir / "annotated_prediction.png"
    mask_id_path = output_dir / "instance_mask_ids.png"
    instance_csv_path = output_dir / "wb_instances.csv"
    image_summary_path = output_dir / "wb_image_summary.csv"

    cv2.imwrite(str(annotated_path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))
    cv2.imwrite(str(mask_id_path), mask_id)  # 16-bit PNG preserves instance IDs.
    per_instance.to_csv(instance_csv_path, index=False)
    pd.DataFrame([{
        "image_width": w,
        "image_height": h,
        "wb_count": count,
        "total_instance_mask_area_px2": total_mask_area,
        "mean_instance_mask_area_px2": round(mean_area, 3),
        "confidence_threshold": float(confidence),
        "nms_iou": float(nms_iou),
    }]).to_csv(image_summary_path, index=False)

    return (
        overlay,
        summary,
        per_instance,
        str(annotated_path),
        str(instance_csv_path),
        str(image_summary_path),
        str(mask_id_path),
    )


with gr.Blocks(title="M18K V2 — WB-only Mushroom Detection") as demo:
    gr.Markdown(
        "# M18K V2 — White Button Mushroom Demo\n"
        "Load a random test image from Google Drive or upload an RGB image. "
        "The WB-only YOLOv8n-seg model predicts instance masks, counts mushrooms, "
        "and measures each predicted mask in px²."
    )
    with gr.Row():
        with gr.Column(scale=1):
            input_image = gr.Image(label="Input RGB image", type="numpy")
            load_button = gr.Button("Load random M18K V2 test image", variant="secondary")
            selected_info = gr.Textbox(label="Selected test image", interactive=False)
            confidence_slider = gr.Slider(0.05, 0.80, value=0.25, step=0.05, label="Confidence threshold")
            iou_slider = gr.Slider(0.30, 0.90, value=0.70, step=0.05, label="NMS IoU threshold")
            boxes_checkbox = gr.Checkbox(value=False, label="Draw bounding boxes")
            run_button = gr.Button("Run WB-only inference", variant="primary")
        with gr.Column(scale=1):
            output_image = gr.Image(label="Predicted instance masks", type="numpy")
            summary_md = gr.Markdown()
    table = gr.Dataframe(label="Per-instance measurements", interactive=False, wrap=True)
    with gr.Accordion("Download outputs", open=False):
        annotated_file = gr.File(label="Annotated PNG")
        instance_csv = gr.File(label="Per-instance CSV")
        summary_csv = gr.File(label="Image summary CSV")
        mask_id_file = gr.File(label="16-bit instance-ID mask PNG")

    # The loader returns (RGB array, filename), so both outputs must be wired.
    load_button.click(load_random_test_image, outputs=[input_image, selected_info])
    run_button.click(
        analyze_image,
        inputs=[input_image, confidence_slider, iou_slider, boxes_checkbox],
        outputs=[output_image, summary_md, table, annotated_file, instance_csv, summary_csv, mask_id_file],
    )
    gr.Markdown(
        "**Model:** YOLOv8n-seg, one class (WB). **Checkpoint:** existing Khang WB-only `best.pt`. "
        "**No training is performed by this demo.**"
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=os.getenv("GRADIO_SHARE", "true").lower() == "true")
