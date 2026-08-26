---
id: "241def34-c50a-438e-85a2-d44882728e9f"
status: "in_review"
slug: "sana-serverless-endpoint"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "Standalone Sana endpoint adapted from nebius/serverless-ai-cookbook. The application tests, pinned image manifests, repository links, and rendered deploy link were checked on 2026-08-26. No live L40S run has established cost or time. The current CMS evaluator rejects media targets and cannot provision Serverless resources, so this eval remains disabled. A schema-compatible Nebius-owned exact-model reference is also required before publication."
github_url: "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/sana-endpoint"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Generate Images with Sana on Serverless AI"
catalog_card_description: "Deploy Sana 1.6B on a preemptible L40S, call an OpenAI-shaped image API, and preserve a validated PNG plus run evidence."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 110
---

# Generate Images with Sana on Serverless AI

Deploy `Efficient-Large-Model/Sana_1600M_1024px_diffusers` behind an OpenAI-shaped image generation API on one preemptible L40S. The project includes the FastAPI server, a pinned Dockerfile, a tested published container, and a smoke test that decodes and validates the generated PNG.

## What you will build

The endpoint exposes:

- `GET /v1/models` as its readiness contract;
- `POST /v1/images/generations` for text-to-image requests;
- bounded controls for image count, dimensions, and inference steps;
- deterministic evidence output using a fixed prompt and seed.

The default is the Apache-2.0 Sana Diffusers checkpoint. Changing `MODEL_ID` can change the applicable model license.

## Prerequisites

- A Nebius project with L40S quota and selected networking
- Docker only if you want to rebuild the supplied image
- Python 3.10 or newer for verification
- Optional `HF_TOKEN` for authenticated Hub downloads

## Deploy

Open the [Sana project folder](https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/sana-endpoint) and click **Deploy on Nebius**. The link pre-fills the tested image `cr.eu-north1.nebius.cloud/e00gw2b7v3pxetvpy7/sana-serve:d315ae1`, port 8000, the L40S preset, a 500 GiB disk, 16 GiB shared memory, and preemptible capacity.

To publish an image you control:

```bash
docker build -t your-registry.example/sana-serve:1 .
docker push your-registry.example/sana-serve:1
```

## Verify

```bash
cd sana-endpoint
export BASE_URL="https://your-endpoint.example"
export API_TOKEN="your-endpoint-token" # only if authentication is enabled
python3 scripts/verify.py
```

The verifier waits for `/v1/models`, submits a seeded 1024×1024 request, checks the PNG signature, and writes `sana.png` plus `run-report.json`. A successful report contains `"status": "passed"`.

The [Nebius Academy deployment video](https://www.youtube.com/watch?v=Ftr-6JF08ZI) explains the common Serverless Endpoint workflow rather than Sana internals.

## Security and troubleshooting

Enable token authentication before exposing this endpoint for production. Supply credentials through `API_TOKEN` and `HF_TOKEN`, never through committed files.

- `502`: wait for model loading and poll `/v1/models`.
- `no CUDA device`: confirm the GPU platform and preset.
- Black output: keep the text encoder and VAE in bf16 as implemented by `serve.py`.
- Invalid size: both sides must be between 256 and 2048 and divisible by 32.

## Clean up

```bash
export ENDPOINT_ID="endpoint-..."
bash scripts/cleanup.sh
```

Delete the endpoint immediately after collecting the verification artifact and run report.
