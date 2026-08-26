# Attribution

This example adapts the physical-AI job concept from [`robotics/smolva-ft-norma-core`](https://github.com/nebius/serverless-ai-cookbook/tree/main/robotics/smolva-ft-norma-core) in `nebius/serverless-ai-cookbook`, licensed under Apache-2.0.

The runtime uses:

- [Hugging Face LeRobot](https://github.com/huggingface/lerobot), through the official `huggingface/lerobot-gpu` image pinned by OCI digest;
- [`lerobot/smolvla_base`](https://huggingface.co/lerobot/smolvla_base), pinned to revision `c83c3163b8ca9b7e67c509fffd9121e66cb96205`;
- [`lerobot/svla_so100_pickplace`](https://huggingface.co/datasets/lerobot/svla_so100_pickplace), pinned to revision `728583b5eaf9e739a7f119e2def466fa1d552402`.

The model and dataset are downloaded from Hugging Face at runtime and are not redistributed here. This repository adds the Nebius one-click job configuration, bounded smoke-training command, Object Storage handoff, artifact verifier, cleanup helper, and offline contract tests.
