# Qwen3-0.6B on Nebius Serverless

Deploy `Qwen/Qwen3-0.6B` as an OpenAI-compatible endpoint on one preemptible Nebius L40S GPU. The deployment uses the pinned `vllm/vllm-openai:v0.19.1` image and needs no custom image build.

[![Deploy on Nebius](https://img.shields.io/badge/Deploy_on-Nebius-6C47FF?style=for-the-badge)](https://console.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-openai%3Av0.19.1&command=python3%20-m%20vllm.entrypoints.openai.api_server%20--model%20Qwen%2FQwen3-0.6B%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

The button pre-fills the image, command, port, L40S platform, one-GPU preset, shared memory, disk, and preemptible capacity. In the console, select your project and networking, review the configuration, and create the endpoint.

## What is deployed

| Setting | Value |
| --- | --- |
| Model | `Qwen/Qwen3-0.6B` |
| Serving API | vLLM OpenAI-compatible server |
| Image | `vllm/vllm-openai:v0.19.1` |
| Compute | `gpu-l40s-a`, `1gpu-8vcpu-32gb` |
| Container port | `8000` |
| Disk / shared memory | `500Gi` / `16Gi` |
| Capacity | preemptible |

Model license: [Apache-2.0](https://huggingface.co/Qwen/Qwen3-0.6B/blob/main/LICENSE). Model source: [Hugging Face](https://huggingface.co/Qwen/Qwen3-0.6B).

## Verify the result

A Nebius endpoint can report `RUNNING` while the model is still downloading. Copy its public URL, then run the smoke test; it waits for `/v1/models`, submits a deterministic chat request, validates the response, and writes `run-report.json`.

```bash
export BASE_URL='https://your-endpoint.example'
# If token authentication is enabled:
export API_TOKEN='your-endpoint-token'
python3 scripts/verify.py
```

Success means `run-report.json` has `"status": "passed"` and `reply.txt` contains non-empty model output. Set `HOURLY_RATE_USD` to add a transparent runtime-cost estimate for the smoke request; the script never invents a rate.

A platform walkthrough is available from [Nebius Academy: How to deploy a Model using Nebius Serverless endpoints](https://www.youtube.com/watch?v=Ftr-6JF08ZI).

## CLI alternative

```bash
nebius ai endpoint create \
  --image vllm/vllm-openai:v0.19.1 \
  --public \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --preemptible \
  --container-port 8000 \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --container-command bash \
  --args '-c python3 -m vllm.entrypoints.openai.api_server --model Qwen/Qwen3-0.6B --host 0.0.0.0 --port 8000'
```

## Security and credentials

The one-click URL leaves endpoint authentication off so the first smoke test is straightforward. Do not use an unauthenticated public endpoint for production. Enable token authentication in the Nebius console and provide the token through `API_TOKEN`; never commit tokens or put them in URLs. `HF_TOKEN` is optional for this public model and should also be supplied as a secret/environment variable if used.

## Troubleshooting

- `502 failed to connect to local service`: the container has not bound port 8000 yet. Keep polling `/v1/models`; `RUNNING` is not the same as API-ready.
- Slow first boot: model weights are still downloading. An optional `HF_TOKEN` can avoid anonymous Hub rate limits.
- `401` or `403`: set `API_TOKEN` to the token configured on the endpoint.
- No capacity: retry without preemptible capacity or select another supported region/preset; this changes cost.

## Cleanup

Delete the endpoint as soon as testing is complete so it stops billing:

```bash
export ENDPOINT_ID='endpoint-...'
bash scripts/cleanup.sh
```

## Validation scope

`bash scripts/check.sh` performs the free local checks. A real end-to-end test requires creating the paid Nebius GPU endpoint; preserve its generated `run-report.json` as the measured evidence for any CMS entry.

## License and provenance

Project code and documentation are Apache-2.0. This project adapts the Qwen3 template in the [Nebius Serverless AI Cookbook](https://github.com/nebius/serverless-ai-cookbook); see [ATTRIBUTION.md](ATTRIBUTION.md).
