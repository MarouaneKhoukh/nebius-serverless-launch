---
id: "4535df76-e913-4990-bcce-b060ed70c71a"
status: "in_review"
slug: kokoro-serverless-tts
internal_content_description: A reproducible Serverless endpoint for Kokoro-82M with audio verification; production cost and timing evidence still require a live Nebius run.
category: serverless-ai
author: marouane-khoukh
model: null
github_url: https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/kokoro-tts-endpoint
video_url: https://www.youtube.com/watch?v=Ftr-6JF08ZI
catalog_card_title: Deploy Kokoro text-to-speech on Serverless
catalog_card_description: Deploy Kokoro-82M as a scalable speech endpoint, generate MP3 or WAV audio, verify the response, and clean up every cloud resource.
estimated_cost_per_run_usd: null
cost_qualifier: approximate
time_to_first_run_minutes: null
time_qualifier: approximately
metrics_verified_at: null
published_at: null
sort: 120
---

## What you will build

This project deploys `hexgrad/Kokoro-82M` behind a Nebius AI Serverless endpoint. The service exposes an OpenAI-style `POST /v1/audio/speech` route and returns either MP3 or WAV audio.

The repository includes the serving image source, deployment instructions, a request example, an automated verifier, cleanup instructions, tests, and CI. It is designed to make the full lifecycle reproducible rather than stopping after the endpoint becomes healthy.

## Before you begin

You need a Nebius project, the Nebius CLI, Docker, permission to push images to Container Registry, and permission to create Serverless endpoints. Create a dedicated API token for the endpoint and keep it outside source control.

The example targets one NVIDIA L40S GPU. Review the current Nebius price before deployment and delete the endpoint after verification.

## Deploy

Clone the linked project folder, follow its README, build and push the container image, and create the endpoint with the supplied resource settings. Wait for the endpoint to report a healthy state before sending traffic.

The container installs the English grapheme-to-phoneme dependencies and `ffmpeg`, maps supported voices and languages explicitly, and validates the requested playback speed.

## Verify the result

Run the included verifier with the endpoint URL and API token. It sends a short synthesis request, saves the returned audio, confirms the content type and file signature, and writes a machine-readable report.

Successful verification proves that the deployed endpoint accepts authenticated requests and produces a usable audio file. Listen to the sample as a final qualitative check.

## Security and production notes

- Store API tokens in environment variables or a secret manager.
- Restrict registry and Serverless permissions to the minimum required roles.
- Add request-size limits, observability, rate limits, and an approved voice policy before production use.
- Treat generated speech as untrusted output when it enters another automated workflow.

## Troubleshooting

If startup fails, inspect the endpoint logs for missing model files, phonemizer libraries, or `ffmpeg`. If synthesis returns an error, confirm the requested voice, language, speed, response format, and authorization header. If the verifier receives HTML or JSON instead of audio, check the endpoint URL and route.

## Clean up

Delete the Serverless endpoint after the test. Remove the container image as well if it is no longer needed. The repository documents both steps so no chargeable resource is left running accidentally.
