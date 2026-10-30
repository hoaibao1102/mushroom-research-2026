# Possible manuscript outline — not a completed paper

1. Introduction: dense mushroom instance segmentation, motivation for RGB-D sensing.
2. Related work: M18K (2025), 2D segmentation, 3D pose, depth fusion, dense object detection.
3. Data: V2 source, provenance, integrity checks, rare-class labels, split independence and leakage limitations.
4. Methods: reproducible RGB YOLO baseline; controlled RGB-D extension if feasible; possible 3D pose task.
5. Experiments: frozen splits, seeds, computing budget, IoU/AP metrics, per-class and size-conditioned analysis.
6. Results: EDA first; model metrics only after real test runs.
7. Discussion: limitations, alternative explanations and practical harvesting relevance.

**No novelty or empirical improvement is asserted.** The original M18K paper already contains 3D pose estimation, so a genuine extension requires a distinct hypothesis and fair comparison.
