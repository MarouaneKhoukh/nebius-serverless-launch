---
id: "4535df76-e913-4990-bcce-b060ed70c71a"
status: "in_review"
slug: "kokoro-serverless-tts"
category: "serverless-ai"
author: "marouane-khoukh"
model: null
internal_content_description: "CMS adaptation of the existing Kokoro-82M one-click endpoint template in nebius/serverless-ai-cookbook. Live L40S and audio-output validation, a Serverless-capable evaluator, a compatible model record, and measured cost and time-to-first-run are still required."
github_url: "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-kokoro-82m"
video_url: "https://www.youtube.com/watch?v=Ftr-6JF08ZI"
catalog_card_title: "Kokoro speech generation, served as an API"
catalog_card_description: "Serve Kokoro-82M through an OpenAI-style speech API estimated at about $0.80 per active hour."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: 10
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 120
---

# Deploy Kokoro-82M text-to-speech on Nebius Serverless

Speech APIs hide a surprisingly long dependency chain: model weights, grapheme-to-phoneme conversion, audio encoding, and an HTTP contract. This recipe packages [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) behind an OpenAI-style endpoint and turns one sentence into an MP3 you can download and hear.

> **Why this matters here:** the endpoint owns the GPU and audio-serving runtime, while callers only choose text, voice, and output format. That makes the same speech interface available to applications without reproducing the model environment on every machine.

## What you'll build

A Nebius Serverless Endpoint that:

- serves the 82M-parameter Kokoro model on one preemptible L40S;
- uses `GET /v1/models` as its readiness signal;
- accepts speech requests at `POST /v1/audio/speech`;
- supports MP3 or WAV output plus voice and speed controls;
- saves the returned bytes as `kokoro-sample.mp3`.

The published image includes English grapheme-to-phoneme support. Its default voice is `af_bella`; other common choices include `af_heart`, `af_nicole`, `am_adam`, `bf_emma`, and `bm_george`.

## Setup

Use a Nebius project and subnet with L40S quota. Open the [Kokoro-82M template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-kokoro-82m), click **Create Endpoint**, and review the published image, port `8000`, `1gpu-8vcpu-32gb` preset, 500 GiB disk, 16 GiB shared memory, and preemptible capacity.

The template leaves authentication off for the first test. Enable token authentication for any shared endpoint and add `Authorization: Bearer $API_TOKEN` when it is enabled.

```bash
export BASE_URL="https://your-endpoint.example"
```

## Choose a voice and response

Wait until the service itself answers:

```bash
curl -sS "$BASE_URL/v1/models"
```

The request below uses the default American English voice and asks for MP3. Keep the input short for the first test so failures are easy to isolate.

```bash
curl -sS -X POST "$BASE_URL/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{"model":"kokoro","input":"Hello from Kokoro on Nebius Serverless.","voice":"af_bella","response_format":"mp3"}' \
  -o kokoro-sample.mp3
```

Voice prefixes and language support must match the image's grapheme-to-phoneme setup. Switching to a voice from another locale without the corresponding language support can produce an error or incorrect pronunciation.

## Run and verify

Verify that the response is non-empty, inspect the detected type, and then listen to it:

```bash
test -s kokoro-sample.mp3
file kokoro-sample.mp3
```

Success means the live request returns a non-empty audio file that a standard player can decode, and the spoken words match the submitted sentence. File checks prove that bytes arrived; listening remains the qualitative test for intelligibility, pronunciation, and voice choice.

If readiness returns `502`, keep waiting for the model and API to load. If MP3 output is empty or fails to decode, inspect endpoint logs for synthesis or `ffmpeg` errors. If a voice fails, return to `af_bella` before changing other settings.

## Clean up and next steps

> **Endpoint lifecycle:** this recipe covers the first deployment and verification. Keep the endpoint running while it serves traffic, stop it when it will be temporarily idle, and delete it only when the service is no longer needed.

Stop the endpoint without deleting it:

```bash
export ENDPOINT_ID="endpoint-..."
nebius ai endpoint stop --id "$ENDPOINT_ID"
```

Restart the stopped endpoint later with `nebius ai endpoint start --id "$ENDPOINT_ID"`. Delete it only when the service is no longer needed:

```bash
nebius ai endpoint delete --id "$ENDPOINT_ID"
```

Stopped endpoints do not incur compute charges, but mounted volumes can continue to be billed. For production, validate every allowed voice and language, cap input length, add authentication and rate limits, and decide whether generated audio is retained. An application that republishes synthetic speech also needs an appropriate disclosure and acceptable-use policy.

> **Planning estimate:** approximately **$0.80 per active hour** and **10 minutes** from creation to the first verified audio file. The hourly figure is a rounded editorial estimate based on the August 27, 2026 [Nebius Compute list rates](https://docs.nebius.com/compute/resources/pricing), a preemptible `gpu-l40s-a` / `1gpu-8vcpu-32gb` endpoint, and a 500 GiB disk. It is not a measured run; actual charges vary with active duration, storage, egress, and taxes.

The linked video demonstrates the common Serverless Endpoint workflow. It does not establish this model's voice quality or measured performance; `metrics_verified_at` remains empty until a controlled run is recorded.
