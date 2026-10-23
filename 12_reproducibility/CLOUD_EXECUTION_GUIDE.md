# Cloud execution guide — future use only

WP-00 does not provision cloud resources, install ML dependencies, upload data or launch training.

Before later execution: obtain explicit compute/cost and data-transfer permission; verify dataset license and consent; choose provider/region/resources/budget; pin the baseline-compatible environment and Git commit; transfer only legally allowed data using checksummed manifests. Keep credentials in local secrets, never Git. Excluded DS-02 data cannot be uploaded or reused.

Use provider secret storage, least privilege and budget limits. Record hardware/drivers/CUDA, Python/dependency snapshot, exact commands, config/seeds/split hashes and timestamps. Mount raw data read-only; keep external test data isolated. Write outputs to versioned run IDs in ignored run/checkpoint storage. Preserve small manifests, metrics and reports in the repository only after privacy/size review.

On completion verify output hashes, download reproducibility evidence, record costs and stop paid resources. A cloud run is not authorized by this guide. Provider-specific commands and working environment locks remain unimplemented until a baseline and resources are selected.
