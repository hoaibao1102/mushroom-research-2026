#!/usr/bin/env python3
"""Inventory a dataset folder and validate common COCO annotation JSON files.

This tool is intentionally dependency-light so it can run before the project
installs PyTorch, Detectron2, MMDetection, or Ultralytics. Pillow is optional
and is only used to read image dimensions for the first N images.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}
ARCHIVE_EXTENSIONS = {".zip", ".rar", ".7z", ".tar", ".gz", ".zst", ".tgz"}


def _read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def _relative_image_lookup(root: Path) -> dict[str, list[Path]]:
    lookup: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            for key in {path.name, path.relative_to(root).as_posix()}:
                lookup.setdefault(key, []).append(path)
    return lookup


def inspect_coco(path: Path, root: Path, image_lookup: dict[str, list[Path]]) -> dict[str, Any] | None:
    try:
        data = _read_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return {"path": str(path), "type": "json_unreadable", "error": str(exc)}

    if not isinstance(data, dict) or not all(key in data for key in ("images", "annotations", "categories")):
        return None

    images = data.get("images") or []
    annotations = data.get("annotations") or []
    categories = data.get("categories") or []
    if not all(isinstance(value, list) for value in (images, annotations, categories)):
        return {"path": str(path), "type": "coco_invalid", "error": "images, annotations and categories must be lists"}

    image_ids = [item.get("id") for item in images if isinstance(item, dict)]
    ann_ids = [item.get("id") for item in annotations if isinstance(item, dict)]
    category_names = {item.get("id"): item.get("name", str(item.get("id"))) for item in categories if isinstance(item, dict)}
    category_counts: Counter[str] = Counter()
    annotations_by_image: Counter[Any] = Counter()
    missing_images: list[str] = []
    duplicate_filenames: list[str] = []
    invalid_boxes: list[int | str] = []
    missing_category_ids: list[int | str] = []
    polygon_annotations = 0
    rle_annotations = 0
    empty_segmentations = 0

    for image in images:
        if not isinstance(image, dict):
            continue
        filename = str(image.get("file_name", ""))
        candidates = image_lookup.get(filename, [])
        if not candidates and filename:
            candidates = image_lookup.get(Path(filename).name, [])
        if not candidates:
            missing_images.append(filename or f"<missing file_name for image id {image.get('id')}>")
        elif len(candidates) > 1:
            duplicate_filenames.append(filename)

    for ann in annotations:
        if not isinstance(ann, dict):
            continue
        image_id = ann.get("image_id")
        annotations_by_image[image_id] += 1
        category_id = ann.get("category_id")
        category_counts[category_names.get(category_id, f"unknown:{category_id}")] += 1
        if category_id not in category_names:
            missing_category_ids.append(ann.get("id", "<no ann id>"))
        bbox = ann.get("bbox")
        if bbox is not None:
            valid_bbox = (
                isinstance(bbox, (list, tuple)) and len(bbox) == 4
                and all(isinstance(x, (int, float)) and math.isfinite(float(x)) for x in bbox)
                and bbox[2] >= 0 and bbox[3] >= 0
            )
            if not valid_bbox:
                invalid_boxes.append(ann.get("id", "<no ann id>"))
        segmentation = ann.get("segmentation")
        if not segmentation:
            empty_segmentations += 1
        elif isinstance(segmentation, list):
            polygon_annotations += 1
        elif isinstance(segmentation, dict):
            rle_annotations += 1

    image_id_set = set(image_ids)
    orphan_annotations = sum(1 for ann in annotations if isinstance(ann, dict) and ann.get("image_id") not in image_id_set)
    try:
        json_rel = path.relative_to(root).as_posix()
    except ValueError:
        json_rel = str(path)

    return {
        "path": json_rel,
        "type": "coco",
        "images": len(images),
        "annotations": len(annotations),
        "categories": [{"id": item.get("id"), "name": item.get("name")} for item in categories if isinstance(item, dict)],
        "annotation_counts_by_category": dict(category_counts),
        "images_with_annotations": len(annotations_by_image),
        "images_without_annotations": max(0, len(images) - len(annotations_by_image)),
        "annotation_segmentations": {
            "polygon": polygon_annotations,
            "rle": rle_annotations,
            "empty": empty_segmentations,
        },
        "checks": {
            "duplicate_image_ids": len(image_ids) - len(set(image_ids)),
            "duplicate_annotation_ids": len(ann_ids) - len(set(ann_ids)),
            "missing_image_files_count": len(missing_images),
            "missing_image_files_sample": missing_images[:20],
            "duplicate_filename_matches_count": len(duplicate_filenames),
            "invalid_bbox_count": len(invalid_boxes),
            "orphan_annotation_count": orphan_annotations,
            "unknown_category_count": len(missing_category_ids),
        },
    }


def inspect_dataset(root: Path, dimension_sample: int = 10) -> dict[str, Any]:
    root = root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise NotADirectoryError(f"Dataset root does not exist or is not a directory: {root}")

    files = [path for path in root.rglob("*") if path.is_file()]
    image_files = [path for path in files if path.suffix.lower() in IMAGE_EXTENSIONS]
    archive_files = [path for path in files if path.suffix.lower() in ARCHIVE_EXTENSIONS or path.name.lower().endswith(".tar.gz")]
    json_files = [path for path in files if path.suffix.lower() == ".json"]
    csv_files = [path for path in files if path.suffix.lower() == ".csv"]
    extension_counts = Counter((path.suffix.lower() or "<no extension>") for path in files)
    image_lookup = _relative_image_lookup(root)

    coco_reports = []
    non_coco_json = []
    for path in json_files:
        report = inspect_coco(path, root, image_lookup)
        if report is None:
            non_coco_json.append(path.relative_to(root).as_posix())
        else:
            coco_reports.append(report)

    dimension_samples: list[dict[str, Any]] = []
    pillow_status = "not_checked"
    if image_files and dimension_sample > 0:
        try:
            from PIL import Image  # type: ignore
            pillow_status = "available"
            for path in image_files[:dimension_sample]:
                try:
                    with Image.open(path) as image:
                        dimension_samples.append({
                            "path": path.relative_to(root).as_posix(),
                            "width": image.width,
                            "height": image.height,
                            "mode": image.mode,
                        })
                except Exception as exc:  # malformed / unsupported image
                    dimension_samples.append({"path": path.relative_to(root).as_posix(), "error": str(exc)})
        except ImportError:
            pillow_status = "not_installed"

    total_bytes = sum(path.stat().st_size for path in files)
    return {
        "root": str(root),
        "summary": {
            "file_count": len(files),
            "total_size_bytes": total_bytes,
            "image_count": len(image_files),
            "archive_count": len(archive_files),
            "json_count": len(json_files),
            "csv_count": len(csv_files),
            "extension_counts": dict(extension_counts),
        },
        "image_dimension_sample": {
            "pillow": pillow_status,
            "sampled": len(dimension_samples),
            "items": dimension_samples,
        },
        "coco_annotations": coco_reports,
        "other_json_files": non_coco_json,
        "csv_files": [path.relative_to(root).as_posix() for path in csv_files],
        "archive_files": [path.relative_to(root).as_posix() for path in archive_files],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Directory containing a downloaded or extracted dataset")
    parser.add_argument("--output", type=Path, default=None, help="Optional JSON report output path")
    parser.add_argument("--dimension-sample", type=int, default=10, help="Number of images to inspect with Pillow (0 disables)")
    args = parser.parse_args()

    try:
        report = inspect_dataset(args.root, dimension_sample=max(0, args.dimension_sample))
    except Exception as exc:
        parser.error(str(exc))
        return 2

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"\nWrote report: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
