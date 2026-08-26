Build a standalone Nebius Serverless Endpoint project for `Qwen/Qwen3-0.6B` using `vllm/vllm-openai:v0.19.1`. Deliver `README.md`, `.env.example`, license and attribution files, verification, cleanup, and check scripts, deterministic tests, and GitHub Actions.

Configure one preemptible `gpu-l40s-a` / `1gpu-8vcpu-32gb` endpoint with port 8000, a 500 GiB disk, and 16 GiB shared memory. The README must include a pre-filled Console link, equivalent CLI command, authentication, readiness, troubleshooting, verification, and cleanup.

Read `BASE_URL` and optional `API_TOKEN` from the environment. The verifier must wait for `/v1/models`, make one deterministic chat-completions request, reject malformed output, save `reply.txt`, and write a JSON report containing `"status": "passed"`. Require `ENDPOINT_ID` before cleanup, keep tests network- and GPU-free, never expose credentials or fabricate live results, and preserve Apache-2.0 attribution to `nebius/serverless-ai-cookbook`.
