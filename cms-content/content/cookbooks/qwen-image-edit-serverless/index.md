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
catalog_card_title: "Qwen image editing, served on demand"
catalog_card_description: "Upload an image with an edit instruction, call Qwen-Image-Edit-2511 through a multipart API, and validate the returned PNG."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 130
---

# Deploy Qwen-Image-Edit-2511 on Nebius Serverless

Image editing is a different API contract from text-to-image generation: the request must carry both pixels and an instruction. This recipe deploys [Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511), uploads a sample image as multipart form data, and decodes the edited result into a PNG.

> **Why this matters here:** vLLM-Omni supplies the multimodal serving layer and Nebius Serverless supplies the H100 lifecycle. You can test instruction-based editing as an API without writing a custom image service first.

## What you'll build

An image-editing endpoint that:

- runs `Qwen/Qwen-Image-Edit-2511` with `vllm/vllm-omni:v0.24.0`;
- uses one preemptible H100 with the `1gpu-16vcpu-200gb` preset;
- exposes `GET /v1/models` for application readiness;
- accepts multipart requests at `POST /v1/images/edits`;
- returns base64-encoded image data that is saved as `qwen-edit.png`.

The template pre-fills port `8000`, a 500 GiB disk, and 16 GiB of shared memory. The model and API route are fixed for this first reproducible test.

## Setup

Use a Nebius project and subnet with H100 quota. Open the [Qwen Image Edit template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-qwen-image-edit-2511), click **Create Endpoint**, and review the image, command, platform, preset, port, storage, and preemptible setting before creating it.

Clone the cookbook so the included sample path resolves:

```bash
git clone --depth 1 https://github.com/nebius/serverless-ai-cookbook.git
cd serverless-ai-cookbook/templates/endpoint-qwen-image-edit-2511
export BASE_URL="https://your-endpoint.example"
```

The template leaves authentication off for the short test. Enable token authentication before shared use and add the bearer header to the requests when enabled.

## The multipart edit request

Do not treat the Nebius resource state as model readiness. Wait until this call returns JSON:

```bash
curl -sS "$BASE_URL/v1/models"
```

Then send the image as the `image` form field and the instruction as `prompt`:

```bash
curl -sS -X POST "$BASE_URL/v1/images/edits" \
  -F "model=Qwen/Qwen-Image-Edit-2511" \
  -F "image=@samples/image.png" \
  -F "prompt=make the sky a dramatic sunset" \
  -F "size=1024x1024" \
  -F "output_format=png" \
  -F "num_inference_steps=20" \
  -F "seed=42" \
  | python3 -c 'import base64,json,sys; p="qwen-edit.png"; open(p,"wb").write(base64.b64decode(json.load(sys.stdin)["data"][0]["b64_json"])); print(f"wrote {p}")'
```

This is not the JSON-only `/v1/images/generations` route. Sending the wrong content type or form-field names is a request error, not a model-quality failure.

## Run and verify

Validate the returned file and report its dimensions:

```bash
python3 -c 'import struct; d=open("qwen-edit.png","rb").read(24); assert d[:8]==b"\x89PNG\r\n\x1a\n"; print("PNG dimensions:", *struct.unpack(">II",d[16:24]))'
```

Success has two layers. The transport check requires valid PNG data with the requested dimensions. The semantic check requires a person to compare `samples/image.png` with `qwen-edit.png` and confirm that the sky changed while unrelated content remained acceptable. A valid PNG alone does not prove a successful edit.

If readiness returns `502`, the model is still downloading or loading. If the request fails, confirm the multipart route and field names. If startup fails, check the H100 preset, port, vLLM-Omni image, and exact model identifier.

## Clean up and next steps

```bash
export ENDPOINT_ID="endpoint-..."
nebius ai endpoint delete "$ENDPOINT_ID"
```

Before accepting user images, enforce MIME type, dimensions and payload size; strip unnecessary metadata; add authentication, timeouts and moderation; and define a retention policy. For generation without an input image, use the Sana text-to-image recipe instead.

The linked video covers the general endpoint workflow. It is not evidence of edit quality, startup time, latency, or cost for this H100 configuration.
