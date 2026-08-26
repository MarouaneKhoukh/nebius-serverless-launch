#!/usr/bin/env bash
set -euo pipefail
: "${BUCKET_ID:?Set BUCKET_ID to the Nebius Object Storage resource ID}"
nebius ai job create \
  --name "smolvla-physical-ai-smoke" \
  --image ghcr.io/astral-sh/uv:python3.12-bookworm-slim \
  --platform gpu-l40s-a \
  --preset 1gpu-24vcpu-96gb \
  --preemptible \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --volume "${BUCKET_ID}:/workspace/output" \
  --container-command bash \
  --args '-lc apt-get update && apt-get install -y --no-install-recommends git ca-certificates ffmpeg && rm -rf /var/lib/apt/lists/* && git clone https://github.com/huggingface/lerobot.git /workspace/lerobot && git -C /workspace/lerobot checkout bf31dd794ffb4f87380aba3912f64421e8352d3c && cd /workspace/lerobot && uv pip install --system -e ".[smolvla,training]" && export RUN_ID=run-$(date +%Y%m%d-%H%M%S) && lerobot-train --policy.path=lerobot/smolvla_base --dataset.repo_id=lerobot/svla_so100_pickplace --batch_size=1 --steps=50 --num_workers=0 --output_dir=/workspace/local-output/$RUN_ID --job_name=smolvla-serverless-smoke --policy.device=cuda --wandb.enable=false && mkdir -p /workspace/output/$RUN_ID && cp -r /workspace/local-output/$RUN_ID/. /workspace/output/$RUN_ID'
