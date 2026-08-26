#!/usr/bin/env bash
set -euo pipefail
: "${BUCKET_ID:?Set BUCKET_ID to the Nebius Object Storage resource ID}"
nebius ai job create \
  --name "axolotl-qwen25-smoke" \
  --image docker.io/axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1 \
  --platform gpu-h100-sxm \
  --preset 1gpu-16vcpu-200gb \
  --preemptible \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --volume "${BUCKET_ID}:/workspace/data" \
  --container-command bash \
  --args '-c curl -fsSL https://raw.githubusercontent.com/MarouaneKhoukh/nebius-serverless-launch/main/axolotl-finetune-job/config.yaml -o /workspace/data/config.yaml && export RUN_ID=run-$(date +%Y%m%d-%H%M%S) && axolotl train /workspace/data/config.yaml && mkdir -p /workspace/data/output/$RUN_ID && cp -r /workspace/output/. /workspace/data/output/$RUN_ID'
