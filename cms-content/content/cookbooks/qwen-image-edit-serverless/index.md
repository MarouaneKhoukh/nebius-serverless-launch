---
id: "8be0a422-5df5-4bc0-927e-96c394de4a04"
status: "in_review"
slug: "qwen-image-edit-serverless"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "A reproducible Qwen Image Edit Serverless endpoint with deterministic input and output checks. Live cost and timing evidence, a media-capable eval adapter, and a schema-compatible Nebius-owned exact-model reference are required before publication."
github_url: "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/qwen-image-edit-endpoint"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Edit images with Qwen on Serverless"
catalog_card_description: "Deploy Qwen Image Edit as a Serverless API, submit an image and instruction, verify the PNG result, and remove the endpoint afterward."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 130
---

# Edit images with Qwen on Serverless

## What you will build

This project deploys `Qwen/Qwen-Image-Edit-2511` with the vLLM Omni image on Nebius AI Serverless. It accepts multipart requests at `POST /v1/images/edits` and returns an edited PNG image.

The linked folder includes deployment settings, a deterministic input-image generator, an endpoint verifier, tests, CI, troubleshooting guidance, and cleanup commands. That makes it suitable for a repeatable launch demo and later regression testing.

## Before you begin

You need a Nebius project, the Nebius CLI, permission to create Serverless endpoints, and an API token for authenticated requests. The documented configuration uses one NVIDIA H100 GPU and the container image `vllm/vllm-omni:v0.24.0`.

Review current prices before creating the endpoint. Image-generation models can have long cold starts and high memory requirements, so keep the verification request deliberately small.

## Deploy

Open the linked folder and follow the README. Use its deployment link or equivalent CLI configuration, set the model identifier, mount any required model-cache volume, and wait until the endpoint is healthy.

Do not expose the endpoint without authentication. For shared environments, use scoped identities and separate launch-test resources from production.

## Verify the result

The verifier creates a simple PPM source image locally, submits it with a short edit instruction, saves the returned PNG, validates its signature and dimensions, and writes a JSON report. This avoids relying on an external copyrighted sample image.

Inspect the generated image as a qualitative check. Automated validation confirms transport and file integrity; it does not prove that every edit instruction will produce a semantically correct result.

## Production considerations

- Enforce image dimensions, MIME types, payload limits, and timeouts.
- Strip unnecessary image metadata and scan uploaded files.
- Add moderation and retention policies suitable for user-provided images.
- Track latency, failure rate, GPU saturation, and cold-start behavior.

## Troubleshooting

If the container does not become ready, inspect logs for incompatible CUDA, insufficient GPU memory, model-download errors, or an incorrect model identifier. If requests fail, check multipart field names, authentication, timeout settings, and the `/v1/images/edits` path.

## Clean up

Delete the endpoint, any dedicated model-cache storage, and other test-only resources after verification. Confirm in the Nebius Console that no launch-test endpoint remains active.
