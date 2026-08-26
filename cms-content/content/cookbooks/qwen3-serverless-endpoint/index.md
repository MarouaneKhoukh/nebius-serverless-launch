---
id: "468a3594-c15e-401e-ac8a-791680c5d486"
status: "in_review"
slug: "qwen3-serverless-endpoint"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "Standalone Serverless Endpoint project created from the Qwen3-0.6B template in nebius/serverless-ai-cookbook. The GitHub project, local tests, container tag, and rendered deploy link were checked on 2026-08-26. Live L40S execution, cost, and time-to-first-run remain unmeasured. The eval is disabled because the current harness targets text-only Token Factory calls and cannot create or test a Nebius Serverless Endpoint. Add a Serverless-capable eval adapter and a successful controlled run before publishing."
github_url: "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/qwen3-endpoint"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Deploy Qwen3-0.6B on a Serverless Endpoint"
catalog_card_description: "Launch a compact Qwen3 chat model on a preemptible L40S and verify its OpenAI-compatible API with a reproducible smoke test."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 100
---

# Deploy Qwen3-0.6B on a Serverless Endpoint

Serve [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B) through an OpenAI-compatible vLLM API without building a custom container. The project pins `vllm/vllm-openai:v0.19.1` and pre-fills a single preemptible L40S, port 8000, 500 GiB of disk, and 16 GiB of shared memory.

## What you will build

A public Nebius Serverless Endpoint with:

- `GET /v1/models` for readiness;
- `POST /v1/chat/completions` for chat requests;
- an optional bearer token for production access;
- an automated smoke test that writes `reply.txt` and `run-report.json`.

The evidence report records the observed readiness-plus-request duration. It estimates cost only when the operator supplies a current hourly rate; the repository does not invent a price.

## Prerequisites

- A Nebius project with L40S quota in a supported region
- Networking selected for the endpoint
- Python 3.10 or newer for the verification script
- Optional `HF_TOKEN` for authenticated Hugging Face downloads

## Deploy

Open the [Qwen3 project folder](https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/qwen3-endpoint) and click **Deploy on Nebius**. Review the pre-filled image, command, GPU preset, port, disk, shared memory, and preemptible setting. Select the project and network before creating the endpoint.

Nebius may show the workload as `RUNNING` while vLLM is still downloading and loading weights. Treat the endpoint as ready only after `/v1/models` returns JSON.

## Verify

Clone the repository and run:

```bash
cd qwen3-endpoint
export BASE_URL="https://your-endpoint.example"
export API_TOKEN="your-endpoint-token" # only if authentication is enabled
python3 scripts/verify.py
```

Success means `reply.txt` contains non-empty model output and `run-report.json` contains `"status": "passed"`.

The accompanying [Nebius Academy video](https://www.youtube.com/watch?v=Ftr-6JF08ZI) demonstrates the Serverless Endpoint deployment workflow.

## Security and troubleshooting

The one-click link leaves authentication off for the initial smoke test. Enable token authentication before production use, store the token in `API_TOKEN`, and never place credentials in a committed file or URL.

- `502 failed to connect to local service`: keep polling `/v1/models`; the container has not bound port 8000 yet.
- `401` or `403`: export the token configured on the endpoint.
- No preemptible capacity: retry later or select regular capacity after reviewing the price change.

## Clean up

```bash
export ENDPOINT_ID="endpoint-..."
bash scripts/cleanup.sh
```

Deletion is part of verification: an endpoint that is left running continues to consume billable resources.
