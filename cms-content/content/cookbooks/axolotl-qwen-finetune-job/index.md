---
id: "003cacac-6b00-455b-a90e-bc2e781616c2"
status: "in_review"
slug: "axolotl-qwen-finetune-job"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS adaptation of the existing Axolotl one-click job template in nebius/serverless-ai-cookbook. The template currently pre-fills H100 and 500 GiB while the separate official Nebius tutorial uses L40S and 450 GiB; DevRel should reconcile that difference. Live validation, a Serverless-job evaluator, a compatible model record, and measured cost and time-to-first-run are also required."
github_url: "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/job-axolotl-finetune"
video_url: "https://www.youtube.com/watch?v=ZjD489E0lls"
catalog_card_title: "Fine-tune Qwen with Axolotl"
catalog_card_description: "Launch an Axolotl QLoRA job from a one-click template and persist the resulting adapter in Object Storage."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 140
---

# Fine-tune Qwen with Axolotl

Use the existing Nebius Serverless Job template to fine-tune Qwen2.5-0.5B with Axolotl and QLoRA. The training job terminates after completion, while the mounted Object Storage bucket preserves the resulting adapter.

> **Why this matters for Serverless:** Fine-tuning becomes a bounded batch workload. Nebius provisions the GPU for the job and releases its compute when the job finishes.

## What you'll run

The template starts the published Axolotl image, downloads the cookbook's training configuration, runs the fine-tune, and copies completed output to a mounted bucket. Its current one-click configuration pre-fills a preemptible H100 and a 500 GiB container disk.

## Setup

Use an existing Nebius project with the required GPU quota, a subnet, and a writable Object Storage bucket mounted at the path shown by the template. Review the dataset, base model, image tag, training configuration, output path, and current pricing before starting the job.

## Run it

Open the linked recipe and use its **Create Job** link or CLI alternative. Select the project, network, and bucket, then start the job and follow its logs. The accompanying video explains the common Serverless fine-tuning workflow rather than serving as proof for this exact configuration.

## Verify and clean up

Success means the job completes and the mounted bucket contains a non-empty adapter plus its configuration. Preserve only artifacts you need. Record cost and runtime from the actual job, then delete the job and remove test-only storage when appropriate.

## Next steps

Evaluate the adapter against a task-specific dataset before treating it as useful. A completed training loop proves the pipeline ran; it does not establish model quality.
