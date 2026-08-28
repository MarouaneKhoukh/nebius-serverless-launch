---
id: "003cacac-6b00-455b-a90e-bc2e781616c2"
status: "in_review"
slug: "axolotl-qwen-finetune-job"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "One-click Nebius Serverless fine-tuning job recipe using Axolotl and 4-bit QLoRA on Qwen2.5-0.5B, with bounded training, Object Storage persistence, adapter verification, and cleanup guidance."
github_url: "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/job-axolotl-finetune"
video_url: "https://www.youtube.com/watch?v=ZjD489E0lls"
catalog_card_title: "Fine-Tune Qwen with Axolotl in a Serverless GPU Job"
catalog_card_description: "Run a bounded 30-step QLoRA fine-tune of Qwen2.5-0.5B, preserve the adapter in Object Storage, and inspect the result."
estimated_cost_per_run_usd: 0.75
cost_qualifier: "approximate"
time_to_first_run_minutes: 20
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 140
---

# Fine-Tune Qwen with Axolotl in a Serverless GPU Job

Fine-tuning tutorials often prove that a training command starts but lose the output when the machine disappears. This recipe runs a deliberately small [Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) QLoRA job and copies the completed adapter into mounted Object Storage before the Serverless Job ends.

> **Why this matters here:** fine-tuning is naturally a bounded batch workload. Nebius provisions the GPU for the run, Axolotl owns the training loop, and Object Storage separates the useful adapter from the disposable compute.

## What you'll run

The [Axolotl template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/job-axolotl-finetune) performs this pipeline:

1. Start the published Axolotl image on one preemptible H100.
2. Download the cookbook's reviewed YAML configuration.
3. Fine-tune Qwen2.5-0.5B for 30 steps with 4-bit QLoRA.
4. Copy the completed output into a timestamped directory in the mounted bucket.
5. Stop the job while retaining the adapter artifacts.

The short run validates the training and persistence path. It is not intended to produce a production-quality language model.

## Setup

You need a Nebius project and subnet with H100 quota plus a writable Object Storage bucket. The template mounts that bucket at `/workspace/data`, uses `axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1`, and pre-fills 500 GiB of disk and 16 GiB of shared memory.

Open the template's **Create Job** link, select the project, network, and bucket, and review the current price and every pre-filled value before creating a billable job. The source configuration uses public model and dataset assets, so an `HF_TOKEN` is optional unless anonymous Hub access is throttled.

## The QLoRA job

The downloaded configuration keeps the launch test small and inspectable:

```yaml
base_model: Qwen/Qwen2.5-0.5B
load_in_4bit: true
adapter: qlora

datasets:
  - path: Salesforce/wikitext
    name: wikitext-2-raw-v1
    split: "train[:2000]"
    type: completion

sequence_len: 128
micro_batch_size: 1
max_steps: 30
output_dir: /workspace/output
```

After training succeeds, the job copies `/workspace/output` into `/workspace/data/output/run-<timestamp>`. That final copy is important: files that exist only on the job's local disk disappear with the compute.

## Run and verify

Start the job from the pre-filled Console form or use the equivalent CLI command in the upstream recipe. Save the returned job ID, then inspect status and logs:

```bash
export JOB_ID="job-..."
nebius ai job get "$JOB_ID"
nebius ai logs "$JOB_ID"
```

A successful infrastructure run reaches a completed state and leaves a timestamped adapter directory in Object Storage. Download that directory and check for a readable `adapter_config.json` and at least one non-empty Safetensors adapter file:

```bash
find ./downloaded-adapter -name adapter_config.json -o -name '*.safetensors'
```

Those files prove that the bounded training pipeline produced an adapter package. They do not prove that the adapter improved Qwen on a useful task; that requires a separate evaluation dataset and baseline comparison.

If the job cannot write output, check the bucket mount and its identity permissions. For out-of-memory failures, confirm that the expected QLoRA configuration and H100 preset were used. If no adapter appears, inspect the final training and copy logs before rerunning.

## Clean up and next steps

```bash
nebius ai job delete "$JOB_ID"
```

Keep the adapter only if you need it, then remove test-only bucket objects and dedicated IAM bindings. The one-click template currently pre-fills H100 and 500 GiB, while a separate Nebius tutorial uses different resources; this draft follows the template and keeps that difference flagged for editorial review.

> **Planning estimate:** approximately **$0.75** and **20 minutes** from creation to a persisted adapter. This is a rounded editorial estimate based on the August 27, 2026 [Nebius Compute list rates](https://docs.nebius.com/compute/resources/pricing), a preemptible `gpu-h100-sxm` / `1gpu-16vcpu-200gb` job, a 500 GiB disk, and deletion after verification. It is not a measured run and excludes taxes, egress, and retained Object Storage.

Next, evaluate the adapter against the untouched base model on representative prompts. The linked video explains the broader Serverless fine-tuning workflow, not the quality or measured performance of this exact 30-step run; `metrics_verified_at` remains empty.
