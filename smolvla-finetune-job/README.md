---
title: Fine-tune SmolVLA in a Nebius Serverless Job
category: robotics
type: job
runtime: nebius-ai-jobs
frameworks:
  - smolvla
  - lerobot
keywords:
  - physical-ai
  - smolvla
  - robotics
  - fine-tuning
difficulty: intermediate
---

# Fine-tune SmolVLA in a Nebius Serverless Job

<!-- factory:deploy -->

<a href="https://console.nebius.com/serverless/job/create?image=marouanekhoukh%2Fsmolvla-nebius%40sha256%3Abfb0ea7cbd47c536f2bd46d885d0b4b2e2750d9f1da2f92cc5a69cc095eaa6a7&amp;command=RUN_ID%3Dsmolvla-%24%28date+%2B%25Y%25m%25d-%25H%25M%25S%29+%26%26+hf+download+lerobot%2Fsmolvla_base+--revision+c83c3163b8ca9b7e67c509fffd9121e66cb96205+--local-dir+%2Ftmp%2Fsmolvla-base+%26%26+lerobot-train+--policy.path%3D%2Ftmp%2Fsmolvla-base+--policy.empty_cameras%3D1+--dataset.repo_id%3Dlerobot%2Fsvla_so100_pickplace+--dataset.revision%3D728583b5eaf9e739a7f119e2def466fa1d552402+--rename_map%3D%22%7B%5C%22observation.images.top%5C%22%3A%5C%22observation.images.camera1%5C%22%2C%5C%22observation.images.wrist%5C%22%3A%5C%22observation.images.camera2%5C%22%7D%22+--batch_size%3D1+--steps%3D50+--num_workers%3D1+--seed%3D42+--log_freq%3D1+--save_freq%3D50+--env_eval_freq%3D0+--eval_steps%3D0+--output_dir%3D%2Ftmp%2F%24RUN_ID+--job_name%3Dsmolvla-serverless-smoke+--policy.device%3Dcuda+--policy.push_to_hub%3Dfalse+--wandb.enable%3Dfalse+%26%26+find+%2Ftmp%2F%24RUN_ID+-type+l+-delete+%26%26+mkdir+-p+%2Ftmp%2Foutput%2F%24RUN_ID+%26%26+cp+-r+%2Ftmp%2F%24RUN_ID%2F.+%2Ftmp%2Foutput%2F%24RUN_ID&amp;platform=gpu-h100-sxm&amp;preset=1gpu-16vcpu-200gb&amp;volume=%2Ftmp%2Foutput&amp;diskSize=500Gi&amp;shmSize=16Gi"><img src="https://img.shields.io/badge/Create_job_on-Nebius-6C47FF?style=for-the-badge" alt="Create job on Nebius"></a>

<!-- /factory:deploy -->

<!-- factory:intro -->

Run a 50-step SmolVLA fine-tuning smoke test on a regular H100 SXM and persist the completed LeRobot checkpoint in Nebius Object Storage.

**Model and dataset licenses:** Apache-2.0 · **Training framework:** [Hugging Face LeRobot](https://github.com/huggingface/lerobot)

<!-- /factory:intro -->

> **Validation status:** A real Nebius H100 job completed all 50 steps and persisted its step-50 checkpoint in Object Storage on 2026-08-27. This validates the bounded pipeline only; it makes no cost, timing, convergence, model-quality, or robot-safety claim.

## What this job proves

The bounded run is designed to check the cloud pipeline: GPU provisioning, pinned model and dataset downloads, LeRobot startup, 50 optimizer steps, checkpoint creation, and Object Storage persistence.

It does not establish manipulation quality or safe behavior on a physical robot. Hardware use requires separate simulation and controlled-lab evaluation.

## Job configuration

| Setting | Value |
| --- | --- |
| Container | `marouanekhoukh/smolvla-nebius@sha256:bfb0ea7cbd47c536f2bd46d885d0b4b2e2750d9f1da2f92cc5a69cc095eaa6a7` |
| Base policy | `lerobot/smolvla_base` at `c83c3163b8ca9b7e67c509fffd9121e66cb96205` |
| Dataset | `lerobot/svla_so100_pickplace` at `728583b5eaf9e739a7f119e2def466fa1d552402` |
| Training bound | 50 steps, batch size 1, seed 42 |
| Compute | `gpu-h100-sxm` / `1gpu-16vcpu-200gb`, regular |
| Container disk | 500 GiB |
| Shared memory | 16 GiB |
| Timeout | 1 hour in the CLI helper |
| Output mount | writable bucket at `/tmp/output` |

The wrapper is built from `Dockerfile.nebius` on the pinned Hugging Face GPU image and changes only the runtime user to root so Nebius can write to the bucket mount.

## Prerequisites

- An existing Nebius project and configured Nebius CLI
- H100 SXM, VM, and networking quota
- A subnet with outbound HTTPS access to Hugging Face
- A writable Nebius Object Storage bucket
- Current Serverless pricing reviewed before creation

The model and dataset are public. If Hugging Face rate limits anonymous downloads, configure `HF_TOKEN` through Nebius secret management rather than placing it in this repository or the deploy URL.

## One-click path

Click **Create job on Nebius**, then:

1. Select your existing project and subnet.
2. Attach a writable Object Storage bucket at `/tmp/output`.
3. Confirm the pinned image, H100 preset, 50-step command, disk, shared memory, timeout, and regular capacity.
4. Review the current estimated charge and create the job only when you are ready.
5. Follow the job logs until training and the final copy complete.

## CLI path

Copy `.env.example` to `.env` without committing it, then set the bucket and subnet resource IDs:

```bash
export BUCKET_ID="storagebucket-..."
export SUBNET_ID="vpcsubnet-..."
bash scripts/create_job.sh
```

The helper prints the job response. Save its job ID and follow logs:

```bash
export JOB_ID="job-..."
nebius ai logs "$JOB_ID" --follow
```

<!-- factory:cli -->

The helper submits the equivalent `nebius ai job create` command with the configuration shown above. Inspect [`scripts/create_job.sh`](scripts/create_job.sh) before running it.

<!-- /factory:cli -->

## Expected artifact

After a successful run, the mounted bucket should contain a timestamped directory such as:

```text
smolvla-YYYYmmdd-HHMMSS/
└── checkpoints/
    └── 000050/
        ├── pretrained_model/
        │   ├── config.json
        │   ├── model.safetensors
        │   └── train_config.json
        └── training_state/
```

The exact checkpoint directory label is controlled by LeRobot. Verification searches the downloaded run directory rather than assuming a single fixed nesting level.

## Verify

Download one completed run directory from Object Storage, then point the offline verifier at it:

```bash
export ARTIFACT_DIR="$PWD/artifacts/smolvla-YYYYmmdd-HHMMSS"
export JOB_ID="job-..."                 # optional report context
export JOB_RUNTIME_SECONDS="..."        # optional observed value
export HOURLY_RATE_USD="..."            # optional current rate you supplied
python3 scripts/verify.py
```

The verifier requires a non-empty `.safetensors` file and `train_config.json`. It checks the model, dataset revision, step count, batch size, and seed recorded in that configuration and writes `run-report.json`.

## Troubleshooting

- **Image pull or startup failure:** confirm the pinned image digest is still available to the selected region.
- **Model or dataset download failure:** confirm outbound HTTPS access; use a managed `HF_TOKEN` only if anonymous access is throttled.
- **CUDA unavailable:** confirm `gpu-h100-sxm` and the `1gpu-16vcpu-200gb` preset.
- **Training configuration rejected:** keep the pinned image and command together; LeRobot CLI fields can change between releases.
- **No checkpoint in the bucket:** confirm the bucket is mounted writable at `/tmp/output`, use the pinned root wrapper image, and inspect the final job log lines.
- **Capacity unavailable:** retry later or choose another regular GPU configuration after reviewing its current price and compatibility.

## Clean up

Delete the completed job when you no longer need it:

```bash
export JOB_ID="job-..."
bash scripts/cleanup.sh
```

The cleanup helper deletes only the specified job. Review the saved checkpoint first, then remove test-only bucket objects or the bucket separately if you no longer need them.

## Local checks

```bash
bash scripts/check.sh
```

These checks require no Nebius credentials, network access, GPU, or paid resources.

## Safety and provenance

A 50-step training run is pipeline validation only. Before using a policy on hardware, evaluate it in simulation and a controlled environment with supervision, motion and force limits, emergency stops, and a rollback plan.

See [ATTRIBUTION.md](ATTRIBUTION.md) for upstream sources and pinned revisions.
