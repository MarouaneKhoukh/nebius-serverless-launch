# Fine-tune SmolVLA on Nebius Serverless Jobs

Run a 50-step physical-AI smoke fine-tune of `lerobot/smolvla_base` on the public `lerobot/svla_so100_pickplace` dataset with a Nebius Serverless L40S job. No robot or local GPU is required: this validates the cloud training and checkpoint path, not behavior on physical hardware.

[![Create job on Nebius](https://img.shields.io/badge/Create_job_on-Nebius-6C47FF?style=for-the-badge)](https://console.nebius.com/serverless/job/create?image=ghcr.io%2Fastral-sh%2Fuv%3Apython3.12-bookworm-slim&command=apt-get%20update%20%26%26%20apt-get%20install%20-y%20--no-install-recommends%20git%20ca-certificates%20ffmpeg%20%26%26%20rm%20-rf%20%2Fvar%2Flib%2Fapt%2Flists%2F*%20%26%26%20git%20clone%20https%3A%2F%2Fgithub.com%2Fhuggingface%2Flerobot.git%20%2Fworkspace%2Flerobot%20%26%26%20git%20-C%20%2Fworkspace%2Flerobot%20checkout%20bf31dd794ffb4f87380aba3912f64421e8352d3c%20%26%26%20cd%20%2Fworkspace%2Flerobot%20%26%26%20uv%20pip%20install%20--system%20-e%20'.%5Bsmolvla%2Ctraining%5D'%20%26%26%20export%20RUN_ID%3Drun-%24(date%20%2B%25Y%25m%25d-%25H%25M%25S)%20%26%26%20lerobot-train%20--policy.path%3Dlerobot%2Fsmolvla_base%20--dataset.repo_id%3Dlerobot%2Fsvla_so100_pickplace%20--batch_size%3D1%20--steps%3D50%20--num_workers%3D0%20--output_dir%3D%2Fworkspace%2Flocal-output%2F%24RUN_ID%20--job_name%3Dsmolvla-serverless-smoke%20--policy.device%3Dcuda%20--wandb.enable%3Dfalse%20%26%26%20mkdir%20-p%20%2Fworkspace%2Foutput%2F%24RUN_ID%20%26%26%20cp%20-r%20%2Fworkspace%2Flocal-output%2F%24RUN_ID%2F.%20%2Fworkspace%2Foutput%2F%24RUN_ID&platform=gpu-l40s-a&preset=1gpu-24vcpu-96gb&volume=%2Fworkspace%2Foutput&diskSize=500Gi&shmSize=16Gi&preemptible=true)

The form pre-fills the base image, pinned LeRobot source revision, official dataset, bounded smoke command, L40S preset, bucket mount path, disk, shared memory, and preemptible capacity. Select a Nebius project, networking, and a writable Object Storage bucket mounted at `/workspace/output` before creating the job.

## Why this fits the launch

This is a one-click, reproducible Serverless Job for a physical-AI workload. It demonstrates Hub dataset acquisition, GPU fine-tuning, checkpoint persistence, verification, and cleanup. The 50-step budget is deliberately a pipeline smoke test; it does not establish manipulation quality, convergence, or hardware readiness.

The original NormaCore cookbook route was adapted because its external SO-101 Parquet URL currently returns an HTTP 500. This repository instead uses the public, Apache-2.0 dataset referenced by the official SmolVLA documentation, eliminating that broken dependency while preserving the physical-AI job story.

## Job contract

| Setting | Value |
| --- | --- |
| Base checkpoint | `lerobot/smolvla_base` |
| Training code | `huggingface/lerobot` commit `bf31dd794ffb4f87380aba3912f64421e8352d3c` |
| Dataset | `lerobot/svla_so100_pickplace`, revision `728583b5eaf9e739a7f119e2def466fa1d552402` at authoring time |
| Smoke budget | 50 steps, batch size 1 |
| Base image | `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` |
| Compute | `gpu-l40s-a`, `1gpu-24vcpu-96gb` |
| Disk / shared memory | `500Gi` / `16Gi` |
| Persistent output | `/workspace/output/run-YYYYmmdd-HHMMSS/` |

The LeRobot source is pinned so code and dependency constraints do not drift. The dataset is downloaded from the Hugging Face Hub by `lerobot-train`. Training writes to local job disk, and only completed output is copied to the mounted bucket.

## CLI path

Create a bucket and export its resource ID:

```bash
nebius storage bucket create --name your-unique-smolvla-bucket
export BUCKET_ID="$(nebius storage bucket get-by-name --name your-unique-smolvla-bucket --format json | jq -r '.metadata.id')"
bash scripts/create_job.sh
```

The bucket is IAM-mounted; no Object Storage secret is placed in the job command. `HF_TOKEN` is optional for the public model and dataset. If anonymous Hub access is throttled, pass the token with Nebius secret management.

## Verify the checkpoint

After the job completes, download one run folder and verify it:

```bash
nebius ai job logs JOB_ID --follow
aws s3 cp --recursive s3://YOUR_BUCKET/RUN_ID ./download/RUN_ID
export ARTIFACT_DIR="$PWD/download/RUN_ID"
export JOB_ID='job-...'
export JOB_RUNTIME_SECONDS='...' # optional measured job value
export HOURLY_RATE_USD='...'      # optional current rate
python3 scripts/verify.py
```

The verifier requires at least one non-empty model `.safetensors` file and a saved training configuration, then writes `run-report.json`. No runtime, cost, or quality number is fabricated.

[Nebius Academy: How to finetune a model using Nebius Serverless Jobs](https://www.youtube.com/watch?v=ZjD489E0lls) explains the same platform workflow; it is a general fine-tuning walkthrough rather than a SmolVLA-specific demo. The [official SmolVLA guide](https://huggingface.co/docs/lerobot/smolvla) documents the model and `lerobot-train` interface.

## Troubleshooting

- `CUDA required` or CPU fallback: confirm the L40S GPU platform and `--policy.device=cuda`.
- Video decoding fails: the job installs `ffmpeg`; retain that package and the `training` extra.
- Hub throttling: provide `HF_TOKEN` through Nebius secret handling.
- No persisted checkpoint: confirm the bucket is mounted writable at `/workspace/output`; the final copy runs only after successful training.
- Preemption: resubmit or choose regular capacity; this changes cost.

## Cleanup

```bash
export JOB_ID='job-...'
bash scripts/cleanup.sh
```

The script deletes only the GPU job. Review the checkpoint and evidence, then remove Object Storage artifacts separately when they are no longer needed.

Run `bash scripts/check.sh` for free local checks. A paid L40S run is still required before marking the eventual CMS entry as live-validated.

## License and provenance

Project code and documentation are Apache-2.0. Upstream code, model, and dataset artifacts retain their own licenses; see [ATTRIBUTION.md](ATTRIBUTION.md).
