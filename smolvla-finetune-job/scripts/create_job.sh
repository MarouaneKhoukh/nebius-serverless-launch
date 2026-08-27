#!/usr/bin/env bash
set -euo pipefail

: "${BUCKET_ID:?Set BUCKET_ID to the writable Nebius Object Storage bucket resource ID}"
: "${SUBNET_ID:?Set SUBNET_ID to the Nebius subnet resource ID}"

IMAGE="${SMOLVLA_IMAGE:-marouanekhoukh/smolvla-nebius@sha256:bfb0ea7cbd47c536f2bd46d885d0b4b2e2750d9f1da2f92cc5a69cc095eaa6a7}"
PLATFORM="${SMOLVLA_PLATFORM:-gpu-h100-sxm}"
PRESET="${SMOLVLA_PRESET:-1gpu-16vcpu-200gb}"
COMMAND='RUN_ID=smolvla-$(date +%Y%m%d-%H%M%S) && hf download lerobot/smolvla_base --revision c83c3163b8ca9b7e67c509fffd9121e66cb96205 --local-dir /tmp/smolvla-base && lerobot-train --policy.path=/tmp/smolvla-base --policy.empty_cameras=1 --dataset.repo_id=lerobot/svla_so100_pickplace --dataset.revision=728583b5eaf9e739a7f119e2def466fa1d552402 --rename_map='\''{\"observation.images.top\":\"observation.images.camera1\",\"observation.images.wrist\":\"observation.images.camera2\"}'\'' --batch_size=1 --steps=50 --num_workers=1 --seed=42 --log_freq=1 --save_freq=50 --env_eval_freq=0 --eval_steps=0 --output_dir=/tmp/$RUN_ID --job_name=smolvla-serverless-smoke --policy.device=cuda --policy.push_to_hub=false --wandb.enable=false && find /tmp/$RUN_ID -type l -delete && mkdir -p /tmp/output/$RUN_ID && cp -r /tmp/$RUN_ID/. /tmp/output/$RUN_ID'

set --
if [[ "${SMOLVLA_DRY_RUN:-0}" == "1" ]]; then
  set -- "$@" --dry-run
fi
if [[ "${SMOLVLA_PREEMPTIBLE:-0}" == "1" ]]; then
  set -- "$@" --preemptible
fi

nebius ai job create "$@" \
  --name "smolvla-serverless-smoke" \
  --subnet-id "$SUBNET_ID" \
  --image "$IMAGE" \
  --platform "$PLATFORM" \
  --preset "$PRESET" \
  --timeout 1h \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --volume "${BUCKET_ID}:/tmp/output:rw" \
  --container-command /bin/bash \
  --args "-lc \"${COMMAND}\""
