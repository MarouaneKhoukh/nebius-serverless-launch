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
catalog_card_title: "Turn text into speech with Kokoro"
catalog_card_description: "Deploy Kokoro-82M from a one-click Serverless template and generate speech through an OpenAI-compatible API."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 120
---

# Turn text into speech with Kokoro

Run [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) as a speech endpoint from the existing Nebius Serverless template. The recipe uses a prepared serving image and an OpenAI-compatible text-to-speech request.

> **Why this matters for Serverless:** The model is small, but speech generation still benefits from an endpoint that owns the runtime, GPU lifecycle, and audio-serving dependencies.

## What you'll deploy

The template starts the published Kokoro serving image on one preemptible L40S. Its API accepts text, voice, speed, language, and response-format settings and returns MP3 or WAV audio.

## Setup

Choose an existing Nebius project, confirm L40S quota, and select networking. Review the prepared container and resource settings before creation. Enable endpoint token authentication before exposing the service beyond a private test.

## Run it

Open the linked recipe, use its pre-filled **Create Endpoint** flow or CLI alternative, and wait until the service is ready. Send the documented short speech request, save the returned audio, and play it to confirm the spoken result.

The accompanying video demonstrates how to deploy a model on Serverless Endpoints; it is not a Kokoro quality or latency benchmark.

## Verify and clean up

Success means the endpoint returns a non-empty MP3 or WAV file that can be decoded and played. Record cost and timing only from the live run. Delete the endpoint when testing is finished.

## Next steps

For production use, validate supported voices and languages, bound text length, add authentication and rate limits, and define how generated audio is retained.
