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

<a href="https://console.nebius.com/serverless/job/create?image=huggingface%2Flerobot-gpu%40sha256%3Adb28375428aa330d2ffac1e0e58ed586041c15e9415df100f9fe0946789d6085&amp;command=RUN_ID%3Dsmolvla-%24%28date%20%2B%25Y%25m%25d-%25H%25M%25S%29%20%26%26%20hf%20download%20lerobot%2Fsmolvla_base%20--revision%20c83c3163b8ca9b7e67c509fffd9121e66cb96205%20--local-dir%20%2Ftmp%2Fsmolvla-base%20%26%26%20lerobot-train%20--policy.path%3D%2Ftmp%2Fsmolvla-base%20--dataset.repo_id%3Dlerobot%2Fsvla_so100_pickplace%20--dataset.revision%3D728583b5eaf9e739a7f119e2def466fa1d552402%20--batch_size%3D1%20--steps%3D50%20--num_workers%3D1%20--seed%3D42%20--log_freq%3D1%20--save_freq%3D50%20--env_eval_freq%3D0%20--eval_steps%3D0%20--output_dir%3D%2Ftmp%2F%24RUN_ID%20--job_name%3Dsmolvla-serverless-smoke%20--policy.device%3Dcuda%20--policy.push_to_hub%3Dfalse%20--wandb.enable%3Dfalse%20%26%26%20mkdir%20-p%20%2Fworkspace%2Foutput%2F%24RUN_ID%20%26%26%20cp%20-r%20%2Ftmp%2F%24RUN_ID%2F.%20%2Fworkspace%2Foutput%2F%24RUN_ID&amp;platform=gpu-l40s-a&amp;preset=1gpu-8vcpu-32gb&amp;volume=%2Fworkspace%2Foutput&amp;diskSize=500Gi&amp;shmSize=16Gi&amp;preemptible=true"><img src="https://img.shields.io/badge/Create_job_on-Nebius-6C47FF?style=for-the-badge" alt="Create job on Nebius"></a>

<!-- /factory:deploy -->

<!-- factory:intro -->

Run a 50-step SmolVLA fine-tuning smoke test on a preemptible L40S and persist the completed LeRobot checkpoint in Nebius Object Storage.

**Model and dataset licenses:** Apache-2.0 · **Training framework:** [Hugging Face LeRobot](https://github.com/huggingface/lerobot)

<!-- /factory:intro -->

> **Validation status:** The repository's offline contract tests pass. A real Nebius L40S run has not yet been completed, so this draft makes no deployment, runtime, cost, convergence, or model-quality claim.

## What this job proves

The bounded run is designed to check the cloud pipeline: GPU provisioning, pinned model and dataset downloads, LeRobot startup, 50 optimizer steps, checkpoint creation, and Object Storage persistence.

It does not establish manipulation quality or safe behavior on a physical robot. Hardware use requires separate simulation and controlled-lab evaluation.

## Job configuration

| Setting | Value |
| --- | --- |
| Container | `huggingface/lerobot-gpu@sha256:db28375428aa330d2ffac1e0e58ed586041c15e9415df100f9fe0946789d6085` |
| Base policy | `lerobot/smolvla_base` at `c83c3163b8ca9b7e67c509fffd9121e66cb96205` |
| Dataset | `lerobot/svla_so100_pickplace` at `728583b5eaf9e739a7f119e2def466fa1d552402` |
| Training bound | 50 steps, batch size 1, seed 42 |
| Compute | `gpu-l40s-a` / `1gpu-8vcpu-32gb`, preemptible |
| Container disk | 500 GiB |
| Shared memory | 16 GiB |
| Timeout | 1 hour in the CLI helper |
| Output mount | writable bucket at `/workspace/output` |

The container digest was resolved from Hugging Face's official GPU image on 2026-08-26. Pinning the digest prevents a nightly image update from silently changing this draft.

## Prerequisites

- An existing Nebius project and configured Nebius CLI
- L40S, VM, and networking quota
- A subnet with outbound HTTPS access to Hugging Face
- A writable Nebius Object Storage bucket
- Current Serverless pricing reviewed before creation

The model and dataset are public. If Hugging Face rate limits anonymous downloads, configure `HF_TOKEN` through Nebius secret management rather than placing it in this repository or the deploy URL.

## One-click path

Click **Create job on Nebius**, then:

1. Select your existing project and subnet.
2. Attach a writable Object Storage bucket at `/workspace/output`.
3. Confirm the pinned image, L40S preset, 50-step command, disk, shared memory, timeout, and preemptible setting.
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
    └── last/
        ├── pretrained_model/
        │   ├── config.json
        │   └── model.safetensors
        └── train_config.json
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
- **CUDA unavailable:** confirm `gpu-l40s-a` and the one-GPU preset.
- **Training configuration rejected:** keep the pinned image and command together; LeRobot CLI fields can change between releases.
- **No checkpoint in the bucket:** confirm the bucket is mounted writable at `/workspace/output` and inspect the final job log lines.
- **Preemption:** resubmit or choose regular capacity after reviewing the price difference.

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
