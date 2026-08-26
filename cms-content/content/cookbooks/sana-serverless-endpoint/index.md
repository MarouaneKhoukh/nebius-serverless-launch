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
catalog_card_title: "Generate images with Sana on Serverless"
catalog_card_description: "Deploy Sana 1.6B from a one-click template and turn a text prompt into a 1024-pixel image on an L40S."
estimated_cost_per_run_usd: null
cost_qualifier: "approximate"
time_to_first_run_minutes: null
time_qualifier: "approximately"
metrics_verified_at: null
published_at: null
sort: 110
---

# Generate images with Sana on Serverless

Deploy `Efficient-Large-Model/Sana_1600M_1024px_diffusers` as a text-to-image endpoint using the existing Nebius Serverless template. The template points to the prepared serving image and includes the request contract needed to generate an image.

> **Why this matters for Serverless:** A GPU-backed image model becomes an HTTP service in your own Nebius project, with lifecycle and access controlled by you.

## What you'll deploy

The template creates a preemptible L40S endpoint from the published Sana serving image. It exposes a readiness route and an OpenAI-shaped image-generation route that returns base64-encoded image data.

## Setup

Use an existing Nebius project with L40S quota and a selected subnet. Review the published container reference and every pre-filled resource before creation. Configure token authentication before shared or production use.

## Run it

Open the linked recipe, launch the pre-filled endpoint, and wait for its readiness route rather than relying only on the resource state. Submit the documented seeded image-generation request, decode the response, and inspect the resulting image.

The linked video shows the general Serverless Endpoint deployment workflow. It is not a Sana-specific benchmark or performance claim.

## Verify and clean up

Success means the live API returns decodable image data with the expected file format. Visual inspection is still required; a valid image file alone does not establish prompt quality. Record only observed cost and timing, then delete the endpoint after the test.

## Next steps

Before accepting user traffic, add input limits, moderation, timeouts, authentication, logging, and a retention policy for generated media.
