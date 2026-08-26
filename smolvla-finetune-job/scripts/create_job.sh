#!/usr/bin/env bash
set -euo pipefail

: "${BUCKET_ID:?Set BUCKET_ID to the writable Nebius Object Storage bucket resource ID}"
: "${SUBNET_ID:?Set SUBNET_ID to the Nebius subnet resource ID}"

IMAGE='huggingface/lerobot-gpu@sha256:db28375428aa330d2ffac1e0e58ed586041c15e9415df100f9fe0946789d6085'
COMMAND='RUN_ID=smolvla-$(date +%Y%m%d-%H%M%S) && hf download lerobot/smolvla_base --revision c83c3163b8ca9b7e67c509fffd9121e66cb96205 --local-dir /tmp/smolvla-base && lerobot-train --policy.path=/tmp/smolvla-base --dataset.repo_id=lerobot/svla_so100_pickplace --dataset.revision=728583b5eaf9e739a7f119e2def466fa1d552402 --batch_size=1 --steps=50 --num_workers=1 --seed=42 --log_freq=1 --save_freq=50 --env_eval_freq=0 --eval_steps=0 --output_dir=/tmp/$RUN_ID --job_name=smolvla-serverless-smoke --policy.device=cuda --policy.push_to_hub=false --wandb.enable=false && mkdir -p /workspace/output/$RUN_ID && cp -r /tmp/$RUN_ID/. /workspace/output/$RUN_ID'

nebius ai job create \
  --name "smolvla-serverless-smoke" \
  --subnet-id "$SUBNET_ID" \
  --image "$IMAGE" \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --preemptible \
  --timeout 1h \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --volume "${BUCKET_ID}:/workspace/output:rw" \
  --container-command /bin/bash \
  --args "-lc \"${COMMAND}\""
