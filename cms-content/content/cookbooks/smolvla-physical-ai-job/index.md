---
id: "1202df8c-70c5-46a8-913a-5e7f248b6cc5"
status: "in_review"
slug: "smolvla-physical-ai-job"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS entry for the SmolVLA one-click job template in MarouaneKhoukh/nebius-serverless-launch. A real regular H100 run completed 50 steps and persisted its checkpoint. A Serverless-job evaluator, a compatible model record, and measured cost and time-to-first-run are still required before publication."
github_url: "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/smolvla-finetune-job"
video_url: "https://www.youtube.com/watch?v=ZjD489E0lls"
catalog_card_title: "Fine-tune a policy for physical AI"
catalog_card_description: "Run a bounded 50-step SmolVLA training job, preserve its checkpoint, and separate cloud-pipeline proof from robot performance."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 150
---

# Fine-tune a physical-AI policy on Nebius Serverless

A robotics checkpoint is only useful when its provenance is clear. This recipe runs a bounded fine-tuning smoke test of Hugging Face's [SmolVLA](https://huggingface.co/lerobot/smolvla_base) policy on the public [SO-100 pick-and-place dataset](https://huggingface.co/datasets/lerobot/svla_so100_pickplace), then persists and inspects the resulting LeRobot checkpoint.

> **Why this matters here:** the cloud pipeline can be tested without a local GPU or a physical robot. Nebius Serverless supplies temporary training compute, while the mounted bucket preserves the result. Pipeline success is not evidence of safe or effective robot behavior.

## What you'll run

The standalone [SmolVLA project](https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/smolvla-finetune-job) creates a job that:

- starts a minimal root wrapper around the official LeRobot GPU image, with both images pinned by digest;
- downloads pinned revisions of `lerobot/smolvla_base` and `lerobot/svla_so100_pickplace`;
- trains for 50 steps with batch size 1 and seed 42 on one regular H100 SXM;
- removes generated checkpoint symlinks and copies the completed run into Object Storage at `/tmp/output/<run-id>`;
- provides an offline verifier and deterministic tests for the artifact contract.

The 50-step bound checks the path from provisioning to persistence. It does not claim convergence or task improvement.

## Setup

You need a Nebius project, a subnet with outbound HTTPS access, H100 SXM quota, and a writable Object Storage bucket. Clone your repository and enter the project:

```bash
git clone https://github.com/MarouaneKhoukh/nebius-serverless-launch.git
cd nebius-serverless-launch/smolvla-finetune-job
```

Review the pinned container, model and dataset revisions, 500 GiB disk, 16 GiB shared memory, one-hour timeout, regular capacity, and current price. Then set only the resource IDs for infrastructure you control:

```bash
export BUCKET_ID="storagebucket-..."
export SUBNET_ID="vpcsubnet-..."
```

## The bounded training contract

These values make the smoke run reviewable and give the verifier something concrete to check:

| Setting | Value |
| --- | --- |
| Policy | `lerobot/smolvla_base` at `c83c3163b8ca9b7e67c509fffd9121e66cb96205` |
| Dataset | `lerobot/svla_so100_pickplace` at `728583b5eaf9e739a7f119e2def466fa1d552402` |
| Training | 50 steps, batch size 1, seed 42 |
| Compute | `gpu-h100-sxm` / `1gpu-16vcpu-200gb`, regular |
| Output | writable bucket mounted at `/tmp/output` |

Pinning does not make the model good; it makes the run traceable. A future change to the model, dataset, or image should be reviewed and tested as a new recipe revision.

## Run and verify

Inspect `scripts/create_job.sh`, then create the billable job only when you are ready:

```bash
bash scripts/create_job.sh
export JOB_ID="job-..."
nebius ai logs "$JOB_ID"
```

After a successful run, download its timestamped output directory from Object Storage and point the verifier at it:

```bash
export ARTIFACT_DIR="$PWD/artifacts/smolvla-YYYYmmdd-HHMMSS"
python3 scripts/verify.py
```

The verifier requires non-empty Safetensors weights and `train_config.json`, checks the recorded dataset revision, step count, batch size, seed, and `smolvla` policy type, then writes `run-report.json`. A passing report proves that the expected checkpoint package exists; it does not score manipulation quality.

If model or dataset downloads fail, check outbound access and cache permissions. If CUDA is unavailable, confirm the H100 SXM platform and preset. If the bucket remains empty, confirm the pinned root wrapper and `/tmp/output` mount, then inspect the final copy step before resubmitting.

## Clean up and next steps

Delete the exact job after saving the logs and required artifact:

```bash
export JOB_ID="job-..."
bash scripts/cleanup.sh
```

Remove test-only bucket objects or the bucket separately when they are no longer needed. For a real robotics experiment, define task-specific data, training length, offline evaluation, and a baseline. Before hardware use, validate in simulation and a controlled environment with human supervision, motion and force limits, emergency stops, and a rollback plan.

> **Planning estimate:** No cost or time estimate is asserted for this regular H100 SXM job. Review the current Nebius price shown for the exact configuration before creation, and use the resulting billing and job timestamps if you need measured figures for your own run.

The linked video explains the general fine-tuning workflow. A real Nebius H100 job completed all 50 steps and persisted 15 step-50 checkpoint objects on 2026-08-27. That validates deployment and artifact persistence only—not cost, timing, convergence, model quality, or robot performance—so `metrics_verified_at` remains empty.
