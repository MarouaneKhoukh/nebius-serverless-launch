---
id: "003cacac-6b00-455b-a90e-bc2e781616c2"
status: "in_review"
slug: "axolotl-qwen-finetune-job"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "A bounded Axolotl QLoRA job with artifact validation and cleanup. This draft follows the serverless-ai-cookbook template's preemptible H100 and 500 GiB configuration; the separate Nebius fine-tuning tutorial currently shows L40S and 450 GiB, so DevRel should resolve that source difference before publication. Live cost and timing evidence, a Serverless-job eval adapter, and a schema-compatible Nebius-owned exact-model reference are also required."
github_url: "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/axolotl-finetune-job"
video_url: "https://www.youtube.com/watch?v=ZjD489E0lls"
catalog_card_title: "Fine-tune Qwen with Axolotl in a GPU job"
catalog_card_description: "Run a short Qwen QLoRA fine-tune with Axolotl, persist the adapter in Object Storage, verify its files, and delete the GPU job."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 140
---

# Fine-tune Qwen with Axolotl in a GPU job

## What you will build

This project runs a deliberately small QLoRA fine-tuning job for Qwen2.5-0.5B with Axolotl on Nebius AI. The job is capped at 30 training steps, writes its adapter locally, and then copies the result to a mounted Object Storage bucket.

The linked folder contains the Axolotl configuration, job definition, identity and bucket setup, an artifact verifier, tests, CI, troubleshooting, and cleanup instructions. The short run validates the cloud training path; it is not intended to produce a production-quality model.

## Before you begin

You need a Nebius project, the Nebius CLI, permission to create GPU jobs, and an Object Storage bucket. The job's service account needs only the permissions required to read and write the selected bucket path.

The reference job uses one NVIDIA H100 and `axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1`. Review image provenance and current Nebius prices before execution.

## Run the job

Follow the README to create the bucket and scoped identity, submit the job, and stream its logs. The training configuration uses a small public dataset, quantized LoRA, a fixed seed, and a 30-step limit so the launch test is bounded.

Outputs are written to local job storage first and copied to the mounted bucket only after training completes. This avoids partially written adapter files being mistaken for a successful result.

## Verify the artifacts

Run the included verifier against the downloaded output directory. It requires a valid `adapter_config.json` and at least one non-empty Safetensors adapter file, checks key configuration fields, and emits a JSON report.

That verification proves the expected adapter package exists. It does not measure model quality; production work should add task-specific evaluation, safety checks, dataset review, and experiment tracking.

## Security and reliability

- Scope the job identity to the exact bucket or prefix used for artifacts.
- Pin images and dependencies, and review them before production runs.
- Keep datasets, tokens, and model licenses under an explicit governance policy.
- Add checkpoints and retry-safe artifact naming for longer training jobs.

## Troubleshooting

If the job cannot read or write the bucket, verify the service-account binding and mount configuration. For out-of-memory errors, confirm quantization settings, sequence length, batch size, and GPU type. If no adapter appears, inspect the final training and copy logs before rerunning.

## Clean up

Delete the completed or failed GPU job after collecting its logs. Retain the adapter only if it is needed, then remove the test bucket or prefix and any dedicated identity bindings created for this run.
