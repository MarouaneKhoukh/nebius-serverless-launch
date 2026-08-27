---
id: "241def34-c50a-438e-85a2-d44882728e9f"
status: "in_review"
slug: "sana-serverless-endpoint"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS adaptation of the existing Sana one-click endpoint template in nebius/serverless-ai-cookbook. Live L40S and media-output validation, a Serverless-capable evaluator, a compatible model record, and measured cost and time-to-first-run are still required."
github_url: "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-sana"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Sana text-to-image on a single L40S"
catalog_card_description: "Turn prompts into 1024px images with Sana 1.6B on an endpoint estimated at about $0.80 per active hour."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: 15
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 110
---

# Run Sana 1.6B text-to-image on Nebius Serverless

Text-to-image demos often end with “the endpoint is healthy.” This recipe goes one step further: it deploys [Sana 1.6B](https://huggingface.co/Efficient-Large-Model/Sana_1600M_1024px_diffusers), submits a fixed prompt and seed, decodes the API response, and leaves you with a real PNG to inspect.

> **Why this matters here:** Sana's weights and image pipeline need a GPU serving environment, but the useful product surface is just an HTTP request. Nebius Serverless keeps that infrastructure boundary behind an endpoint you can create and delete with the workload.

## What you'll build

A text-to-image endpoint that:

- serves the Apache-2.0 Sana Diffusers checkpoint on one preemptible L40S;
- exposes `GET /v1/models` for readiness;
- accepts JSON at `POST /v1/images/generations`;
- returns base64-encoded PNG data in `data[0].b64_json`;
- produces a local `sana.png` from a seeded 1024×1024 request.

The pre-built image supports overrides such as `MODEL_ID`, `IMAGE_SIZE`, `INFERENCE_STEPS`, and `GUIDANCE_SCALE`. Changing the model can also change the applicable license, so keep the default for the first run.

## Setup

Use a Nebius project and subnet with L40S quota. Open the [Sana template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-sana), click **Create Endpoint**, and review the pre-filled published image, port `8000`, `1gpu-8vcpu-32gb` preset, 500 GiB disk, 16 GiB shared memory, and preemptible setting.

The quick test template leaves authentication off. Enable token authentication before exposing the endpoint beyond a short controlled test, and add its bearer header to the commands if you enable it.

```bash
export BASE_URL="https://your-endpoint.example"
```

## The image request

Wait for the application, not just the resource state:

```bash
curl -sS "$BASE_URL/v1/models"
```

Then submit the cookbook's fixed prompt and seed. The seed makes repeated requests easier to compare; it does not guarantee identical output across a changed image, model revision, or runtime.

```bash
curl -sS -X POST "$BASE_URL/v1/images/generations" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a red fox in a snowy pine forest at golden hour","size":"1024x1024","seed":42}' \
  | python3 -c 'import base64,json,sys; p="sana.png"; open(p,"wb").write(base64.b64decode(json.load(sys.stdin)["data"][0]["b64_json"])); print(f"wrote {p}")'
```

## Run and verify

Check the file without requiring an image-processing package:

```bash
python3 -c 'import struct; d=open("sana.png","rb").read(24); assert d[:8]==b"\x89PNG\r\n\x1a\n"; print("PNG dimensions:", *struct.unpack(">II",d[16:24]))'
```

Success means the response decodes, the PNG signature is correct, the reported dimensions match the requested size, and the image opens. Visual inspection is still essential: transport and file-integrity checks cannot tell you whether the fox, scene, or composition is good.

If `/v1/models` returns `502`, the model is still loading. If the container reports no CUDA device, check the platform and preset. Black or empty output can indicate an incompatible dtype override; the published image keeps the text encoder and VAE in bf16 and the transformer in fp16.

## Clean up and next steps

```bash
export ENDPOINT_ID="endpoint-..."
nebius ai endpoint stop --id "$ENDPOINT_ID"
```

Keep it running while it serves traffic, or restart the stopped endpoint later with `nebius ai endpoint start --id "$ENDPOINT_ID"`. Delete it only when the service is no longer needed:

```bash
nebius ai endpoint delete --id "$ENDPOINT_ID"
```

Stopped endpoints do not incur compute charges, but mounted volumes can continue to be billed. Before handling user prompts, add authentication, request-size and dimension limits, timeouts, moderation, logging, and an image-retention policy. For image-to-image work rather than generation from text, continue with the Qwen Image Edit recipe.

> **Planning estimate:** approximately **$0.80 per active hour** and **15 minutes** from creation to the first verified PNG. The hourly figure is a rounded editorial estimate based on the August 27, 2026 [Nebius Compute list rates](https://docs.nebius.com/compute/resources/pricing), a preemptible `gpu-l40s-a` / `1gpu-8vcpu-32gb` endpoint, and a 500 GiB disk. It is not a measured run; actual charges vary with active duration, storage, egress, and taxes.

The linked video covers the general endpoint deployment flow. This draft does not claim a measured startup time, generation latency, cost, or image-quality result; `metrics_verified_at` remains empty until the recipe is run and recorded on Nebius.
