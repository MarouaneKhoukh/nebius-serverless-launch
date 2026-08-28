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
catalog_card_title: "Build an OpenAI-compatible chat API"
catalog_card_description: "Bring up Qwen3-0.6B behind vLLM, verify the chat API, and keep it available for about $0.80 per active hour."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: 10
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 100
---

# Build an OpenAI-compatible chat API on Nebius Serverless

An endpoint marked `RUNNING` is not useful until it can answer a request. This recipe takes the compact [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) model from a pre-filled Nebius Serverless form to a real OpenAI-compatible chat response, with an explicit readiness check and cleanup at the end.

> **Why this matters here:** vLLM already provides the serving layer, while Nebius Serverless owns the GPU lifecycle. You get a familiar chat API in your own project without building a container or maintaining a VM.

## What you'll build

A Nebius Serverless Endpoint that:

- serves `Qwen/Qwen3-0.6B` with `vllm/vllm-openai:v0.19.1`;
- uses one preemptible L40S with the `1gpu-8vcpu-32gb` preset;
- exposes `GET /v1/models` as the application-readiness check;
- accepts chat requests at `POST /v1/chat/completions`;
- saves both the complete JSON response and the assistant text locally.

The template pre-fills port `8000`, a 500 GiB container disk, and 16 GiB of shared memory. Those are deployment inputs, not measured performance claims.

## Setup

You need a Nebius project, a subnet, permission and quota for an L40S endpoint, and the [Qwen3 template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-vllm-qwen3-0-6b). Open its **Create Endpoint** link, select your project and network, and review every pre-filled field before creating a billable resource.

The template leaves authentication off for the first test. Keep that endpoint short-lived and enable token authentication before shared or production use. If authentication is enabled, add `Authorization: Bearer $API_TOKEN` to both requests below.

After creation, copy the public endpoint URL:

```bash
export BASE_URL="https://your-endpoint.example"
```

## The readiness contract

Nebius can report the resource as `RUNNING` while vLLM is still downloading and loading the model. Treat the API as ready only when this returns JSON:

```bash
curl -sS "$BASE_URL/v1/models"
```

A temporary `502 failed to connect to local service` means the Serverless tunnel exists but the container has not bound port `8000` yet. Wait and retry; do not send the chat request based on the resource state alone.

## Run and verify

Send a small, low-temperature request and keep the raw response:

```bash
curl -sS -X POST "$BASE_URL/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen/Qwen3-0.6B","messages":[{"role":"user","content":"Say hello in one short sentence."}],"max_tokens":64,"temperature":0.2}' \
  | tee reply.json

python3 -c 'import json; p=json.load(open("reply.json")); t=p["choices"][0]["message"]["content"]; assert t.strip(); open("reply.txt","w").write(t); print(t)'
```

Success means `reply.json` is valid JSON and `reply.txt` contains a non-empty assistant message returned by the live endpoint. The wording itself can vary; the recipe does not pretend the response is deterministic.

If the request returns `401` or `403`, use the token configured for this endpoint. If preemptible capacity is unavailable, retry later or review the current price before selecting regular capacity.

## Clean up and next steps

> **Endpoint lifecycle:** this recipe covers the first deployment and verification. Keep the endpoint running while it serves traffic, stop it when it will be temporarily idle, and delete it only when the service is no longer needed.

Stop the endpoint without deleting it:

```bash
export ENDPOINT_ID="endpoint-..."
nebius ai endpoint stop --id "$ENDPOINT_ID"
```

Restart the same endpoint later with `nebius ai endpoint start --id "$ENDPOINT_ID"`. Delete it only when you no longer need the service:

```bash
nebius ai endpoint delete --id "$ENDPOINT_ID"
```

Stopped endpoints do not incur compute charges, but mounted volumes can continue to be billed. For a longer-lived service, add token authentication, request limits, logs and metrics, and an explicit capacity decision. To customize a model before serving it, continue with the Axolotl QLoRA recipe in this catalog.

> **Planning estimate:** approximately **$0.80 per active hour** and **10 minutes** from creation to the first verified reply. The hourly figure is a rounded editorial estimate based on the August 27, 2026 [Nebius Compute list rates](https://docs.nebius.com/compute/resources/pricing), a preemptible `gpu-l40s-a` / `1gpu-8vcpu-32gb` endpoint, and a 500 GiB disk. It is not a measured run; actual charges vary with active duration, storage, egress, and taxes.

The linked video demonstrates the common Serverless Endpoint flow. It is not evidence of this recipe's startup time, inference latency, or cost; `metrics_verified_at` remains empty until a controlled Nebius run records them.
