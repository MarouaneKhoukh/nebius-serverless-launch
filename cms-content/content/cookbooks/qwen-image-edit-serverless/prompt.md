Build a standalone Nebius Serverless Endpoint project for `Qwen/Qwen-Image-Edit-2511` using `vllm/vllm-omni:v0.24.0`. Deliver `README.md`, environment example, verification and cleanup scripts, deterministic tests, and GitHub Actions.

Expose multipart image editing at `POST /v1/images/edits`. Document a one-H100 deployment with a pre-filled Console link and equivalent CLI command, authentication, model caching, request examples, payload limits, cold starts, troubleshooting, and cleanup of the endpoint and test-only storage.

The verifier must generate a small PPM input locally, submit it with an edit instruction, save the PNG response, validate status, content type, PNG signature, and dimensions, and write a JSON report. Keep local tests credential- and network-free, make the live smoke test opt-in, never commit tokens, and never fabricate cost, timing, or deployment evidence.
