Create a standalone Nebius AI Serverless project that deploys `Qwen/Qwen-Image-Edit-2511` with `vllm/vllm-omni:v0.24.0` and exposes multipart image editing at `POST /v1/images/edits`.

Document a single-H100 deployment, the required model configuration, authenticated access, health checks, cold-start expectations, and any model-cache storage. Provide both a one-click Nebius Console path where supported and an equivalent CLI path. Include exact request examples and explicit cleanup for the endpoint and test-only storage. Do not commit tokens, fabricate performance figures, or claim that an unexecuted deployment was verified.

Add a deterministic verifier that generates a small PPM input without external assets, submits the image and a concise edit prompt, saves the response as PNG, validates the HTTP status, content type, PNG signature, and decodable dimensions, and writes a JSON report. Use short timeouts for local unit tests and a configurable longer timeout for the opt-in live smoke test.

Add tests for request construction, authentication headers, response validation, and report generation. Add credential-free CI for all local checks. The README must cover payload and MIME limits, image security, moderation, observability, common CUDA or memory failures, and how to confirm that all chargeable resources have been removed.
