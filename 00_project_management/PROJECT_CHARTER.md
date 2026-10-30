# Project charter — Team 10

## Problem and motivation

In dense mushroom cultivation scenes, 2D detection and instance segmentation must localize many tightly clustered mushrooms. M18K provides an opportunity to study image annotation integrity and RGB-D sensing, and later to test whether depth improves segmentation or helps estimate physical pose. Any harvesting benefit is a potential application, not a measured result.

## Active working scope (30 October 2026)

- Dataset: M18K V2, **working candidate C03**, pending team approval, provenance/license completion and QC closure.
- Reference: Zakeri et al. (2025), *M18K: A Multi-Purpose Real-World Dataset for Mushroom Detection, 3D Pose Estimation, and Growth Monitoring*.
- Completed: executed Colab V2 dataset audit and initial EDA, saved and summarized in `09_results/`.
- Not yet completed: full leakage audit, human label review, YOLO model training, held-out evaluation, independent replication or 3D model experiments.

## Core research question

Can a documented RGB segmentation baseline be reproduced on M18K V2 with robust held-out evaluation, and does adding depth information improve performance on crowded or small mushroom instances under controlled comparisons?

## Method

Validate metadata and labels → analyze class/instance distributions → inspect RGB/depth pairing → audit leakage and group independence → freeze dataset/split strategy → train RGB baseline → evaluate on unseen test → investigate depth/3D hypotheses if justified.

## Boundaries and integrity

Keep the project's shared directory structure. Do not put raw images/depth/huge annotation JSON files, checkpoints, credentials or private farm imagery in Git. Do not claim numerical paper reproduction from V2 results without matching its protocol. Formal approvals, legal license conclusions and human visual label adjudication cannot be automated from the uploaded notebook.

## Success criteria

Reproducible data and split manifests, transparent per-class scores, failure-case analysis, versioned model configuration, honest limitations and a scientifically fair comparison. An improvement is not required; a null or negative RGB-D result is meaningful.
