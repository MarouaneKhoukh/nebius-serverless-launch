---
id: "8be0a422-5df5-4bc0-927e-96c394de4a04"
status: "in_review"
slug: "qwen-image-edit-serverless"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS adaptation of the existing Qwen-Image-Edit-2511 one-click endpoint template in nebius/serverless-ai-cookbook. Live H100 and image-edit validation, a media-capable Serverless evaluator, a compatible model record, and measured cost and time-to-first-run are still required."
github_url: "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-qwen-image-edit-2511"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Edit images with Qwen on Serverless"
catalog_card_description: "Deploy Qwen Image Edit from a one-click template, upload an image with an instruction, and save the edited result."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 130
---

# Edit images with Qwen on Serverless

Deploy [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) with vLLM-Omni using the existing Nebius one-click template. Once ready, the endpoint accepts an image and a natural-language edit instruction.

> **Why this matters for Serverless:** A large image-editing model can run as an on-demand API in your Nebius project without writing a separate serving application.

## What you'll deploy

The template runs `vllm/vllm-omni:v0.24.0` with one preemptible H100 and serves the model on port 8000. Image editing uses multipart `POST /v1/images/edits`; the response contains base64-encoded image data.

## Setup

Use an existing Nebius project with H100 quota and appropriate networking. Review the GPU, disk, shared-memory, preemptible-capacity, and container settings before creation. Enable token authentication before shared use.

## Run it

Open the linked template, create the endpoint, and poll `GET /v1/models` until the API is actually ready. Then run the recipe's multipart example with its included sample image and save the decoded PNG response.

The linked video covers the common Serverless Endpoint workflow, not this model's image quality or resource requirements.

## Verify and clean up

Success means the API returns decodable PNG data and the saved file opens as an image. Inspect the edit itself because transport checks do not prove semantic quality. Record only observed cost and timing, then delete the endpoint.

## Next steps

Before handling user uploads, add authentication, MIME and size checks, request limits, timeouts, moderation, metadata handling, and a media-retention policy.
