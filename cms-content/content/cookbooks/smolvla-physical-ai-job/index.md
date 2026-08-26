---
id: "1202df8c-70c5-46a8-913a-5e7f248b6cc5"
status: "in_review"
slug: "smolvla-physical-ai-job"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS entry for the new SmolVLA one-click job template staged in MarouaneKhoukh/nebius-serverless-launch. The official LeRobot GPU image is pinned by digest and the model and dataset revisions are pinned. A real L40S run, a Serverless-job evaluator, a compatible model record, and measured cost and time-to-first-run are required before publication."
github_url: "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/smolvla-finetune-job"
video_url: "https://www.youtube.com/watch?v=ZjD489E0lls"
catalog_card_title: "Fine-tune SmolVLA in a Serverless Job"
catalog_card_description: "Run a bounded SmolVLA physical-AI fine-tune on an L40S and preserve the checkpoint in Object Storage."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 150
---

# Fine-tune SmolVLA in a Serverless Job

Run a bounded fine-tuning smoke test of Hugging Face's [SmolVLA](https://huggingface.co/lerobot/smolvla_base) physical-AI policy on the public [SO-100 pick-and-place dataset](https://huggingface.co/datasets/lerobot/svla_so100_pickplace). The new template uses an official LeRobot GPU image and persists its checkpoint in Nebius Object Storage.

> **Why this matters for Serverless:** Robotics training can use cloud GPUs without requiring a robot or local GPU during the pipeline test. The result is a checkpoint—not evidence that a policy is safe or effective on hardware.

## What you'll run

The template starts one preemptible L40S, downloads pinned model and dataset revisions, and runs 50 training steps with batch size 1 and a fixed seed. It saves the final LeRobot checkpoint to a bucket mounted at `/workspace/output`.

## Setup

Use an existing Nebius project with L40S quota, a subnet, and a writable Object Storage bucket. Review the pinned container digest, model revision, dataset revision, training bounds, timeout, storage mount, and current pricing before starting the job.

## Run it

Open the linked recipe and use its pre-filled **Create Job** link or CLI helper. Select the project, network, and bucket, start the job, and follow its logs through model download, dataset loading, 50 training steps, checkpoint creation, and output copy.

The linked video explains the general Serverless Jobs fine-tuning workflow. It is not evidence of SmolVLA convergence or robot performance.

## Verify and clean up

Success means the job completes and Object Storage contains a LeRobot training configuration and non-empty model weights. The included verifier checks those artifacts without making quality claims. Record cost and runtime only from the live job, then remove the job and any test-only artifacts you no longer need.

## Next steps

Longer training requires task-specific hyperparameters and evaluation. Before using a policy on hardware, validate it in simulation and then in a controlled environment with supervision, motion limits, emergency stops, and a rollback plan.
