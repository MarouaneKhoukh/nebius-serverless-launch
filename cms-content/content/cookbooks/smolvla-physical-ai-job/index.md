---
id: "1202df8c-70c5-46a8-913a-5e7f248b6cc5"
status: "in_review"
slug: smolvla-physical-ai-job
internal_content_description: An adapted physical-AI training template using official LeRobot assets because the original external dataset endpoint is unavailable; live Nebius evidence is pending.
category: serverless-ai
author: marouane-khoukh
model: null
github_url: https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/smolvla-finetune-job
video_url: https://www.youtube.com/watch?v=ZjD489E0lls
catalog_card_title: Fine-tune SmolVLA for physical AI in a GPU job
catalog_card_description: Run a short SmolVLA fine-tune with LeRobot on Nebius, validate the saved checkpoint, and learn where simulation ends and robot testing begins.
estimated_cost_per_run_usd: null
cost_qualifier: approximate
time_to_first_run_minutes: null
time_qualifier: approximately
metrics_verified_at: null
published_at: null
sort: 150
---

## What you will build

This physical-AI project runs a short SmolVLA fine-tuning job with Hugging Face LeRobot on Nebius. It uses the public `lerobot/svla_so100_pickplace` dataset, performs 50 training steps with batch size 1, persists the checkpoint, and validates the expected files.

The source template was adapted because its original external Parquet endpoint is unavailable. This version uses the official LeRobot training interface, pins the LeRobot source revision, and records the dataset revision used when the recipe was authored.

## What this demo proves

The job verifies that Nebius can provision the GPU workload, load the robotics dataset, run the training loop, and preserve a SmolVLA checkpoint. No physical robot is required for the cloud smoke test.

It does not prove safe or reliable real-world robot behavior. Before deployment on hardware, evaluate the policy in simulation and a controlled lab with human supervision, limits, emergency stops, and a documented rollback procedure.

## Before you begin

You need a Nebius project, the Nebius CLI, permission to create GPU jobs, and Object Storage for the output. The reference configuration uses one NVIDIA L40S GPU and pins LeRobot to commit `bf31dd794ffb4f87380aba3912f64421e8352d3c`.

The dataset revision recorded at authoring time is `728583b5eaf9e739a7f119e2def466fa1d552402`. Confirm the dataset license, access, and revision before running the job.

## Run and monitor

Follow the linked README to configure the scoped identity and output storage, submit the job, and monitor logs. The command uses the official LeRobot training CLI with a fixed seed, 50 steps, and batch size 1 to bound the launch test.

The job copies the completed checkpoint to Object Storage only after training succeeds. Keep logs and the verifier report together with the artifact so later reviewers can trace how it was produced.

## Verify the checkpoint

The included verifier checks that the training directory contains the expected policy configuration and non-empty model weights, validates important metadata, and creates a machine-readable report. Unit tests exercise this logic without a GPU.

## Troubleshooting

For dataset errors, confirm the repository identifier, revision, network access, and cache permissions. For memory failures, keep batch size at 1 and verify the L40S resource configuration. If the checkpoint is missing, inspect the final training logs and Object Storage copy step.

## Clean up

Delete the GPU job after collecting its logs and verification report. Remove test-only checkpoints, buckets or prefixes, and dedicated IAM bindings when they are no longer needed.
