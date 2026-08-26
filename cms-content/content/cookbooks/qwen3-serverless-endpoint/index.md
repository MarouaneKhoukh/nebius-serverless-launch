---
id: "468a3594-c15e-401e-ac8a-791680c5d486"
status: "in_review"
slug: "qwen3-serverless-endpoint"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS adaptation of the existing Qwen3-0.6B one-click template in nebius/serverless-ai-cookbook. Live L40S validation, a Serverless-capable evaluator, a compatible model record, and measured cost and time-to-first-run are still required before publication."
github_url: "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-vllm-qwen3-0-6b"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Deploy Qwen3-0.6B on Serverless"
catalog_card_description: "Launch a compact Qwen3 model from a one-click Serverless template and call its OpenAI-compatible chat API."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 100
---

# Deploy Qwen3-0.6B on Serverless

Run the compact [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) model behind an OpenAI-compatible API without building or operating a custom serving stack. The linked Serverless template supplies the container, startup command, GPU configuration, test request, and cleanup guidance.

> **Why this matters for Serverless:** The model runs in your Nebius project as a managed endpoint. You control its compute, networking, authentication, lifetime, and resulting usage charges.

## What you'll deploy

The template starts `vllm/vllm-openai:v0.19.1` on one preemptible L40S and serves `Qwen/Qwen3-0.6B` on port 8000. It exposes `GET /v1/models` for readiness and `POST /v1/chat/completions` for inference.

## Setup

You need an existing Nebius project, permission and quota for an L40S Serverless Endpoint, and a suitable subnet. Review the selected resources and current pricing before creating anything. Enable token authentication for any endpoint that should not be publicly callable.

## Run it

Open the linked template and choose either its pre-filled **Create Endpoint** link or the documented CLI command. Select your project and networking, create the endpoint, then wait until `/v1/models` returns JSON. A `RUNNING` resource can still be downloading and loading model weights.

Send the template's short chat-completions request and inspect the actual model reply. The accompanying video demonstrates the common Serverless Endpoint flow rather than this model alone.

## Verify and clean up

Success means the live endpoint returns a non-empty assistant message from `POST /v1/chat/completions`. Record cost and timing only from the controlled run. Delete the endpoint when the test is complete so it no longer consumes resources.

## Next steps

Add production authentication, request limits, observability, and capacity choices only after the basic template has been validated in the intended region.
