# Attribution

This repository adapts the physical-AI job concept from `robotics/smolva-ft-norma-core` in [nebius/serverless-ai-cookbook](https://github.com/nebius/serverless-ai-cookbook) at commit `bab94ade937a47b082c34f1a953aa71b8a199d1b`, licensed under Apache-2.0.

The runnable path uses [huggingface/lerobot](https://github.com/huggingface/lerobot) commit `bf31dd794ffb4f87380aba3912f64421e8352d3c`, the `lerobot/smolvla_base` checkpoint, and the `lerobot/svla_so100_pickplace` dataset. Each is consumed from its upstream source and is not redistributed here.

Changes include replacement of a currently failing external Parquet URL with the official SmolVLA dataset route, bounded one-click training, immutable source pinning, IAM-mounted output, artifact verification, explicit physical-validation limits, cleanup safeguards, and CI.
