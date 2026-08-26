# Qwen Image Edit on Nebius Serverless

Deploy `Qwen/Qwen-Image-Edit-2511` as an instruction-based image editing endpoint on one preemptible Nebius H100 GPU. The endpoint uses the pinned `vllm/vllm-omni:v0.24.0` image and its OpenAI-shaped multipart image-edit API.

[![Deploy on Nebius](https://img.shields.io/badge/Deploy_on-Nebius-6C47FF?style=for-the-badge)](https://console.nebius.com/serverless/endpoint/create?image=vllm%2Fvllm-omni%3Av0.24.0&command=vllm%20serve%20Qwen%2FQwen-Image-Edit-2511%20--omni%20--host%200.0.0.0%20--port%208000&targetPort=8000&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

The link pre-fills the image, model command, port, H100 preset, disk, shared memory, and preemptible capacity. Select the Nebius project and networking before creating the endpoint.

## Deployment contract

| Setting | Value |
| --- | --- |
| Model | `Qwen/Qwen-Image-Edit-2511` |
| Image | `vllm/vllm-omni:v0.24.0` |
| API | multipart `POST /v1/images/edits` |
| Compute | `gpu-h100-sxm`, `1gpu-16vcpu-200gb` |
| Port | `8000` |
| Disk / shared memory | `500Gi` / `16Gi` |
| Capacity | preemptible |

Model source and license: [Qwen/Qwen-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511) (Apache-2.0).

## Verify the result

The smoke test waits for `/v1/models`, creates a deterministic local PPM test image, calls `/v1/images/edits`, validates and decodes the returned PNG, and records `run-report.json`.

```bash
export BASE_URL='https://your-endpoint.example'
# If endpoint token authentication is enabled:
export API_TOKEN='your-endpoint-token'
python3 scripts/verify.py
```

Success produces `qwen-edit.png` and a report with `"status": "passed"`. Set `HOURLY_RATE_USD` only to a current rate you obtained from Nebius; the script then calculates an estimate for the observed elapsed time.

The general deployment flow is shown in [Nebius Academy: How to deploy a Model using Nebius Serverless endpoints](https://www.youtube.com/watch?v=Ftr-6JF08ZI). The video demonstrates the same Serverless Endpoints workflow, although not this image-edit model specifically.

## CLI alternative

```bash
nebius ai endpoint create \
  --image vllm/vllm-omni:v0.24.0 \
  --public \
  --platform gpu-h100-sxm \
  --preset 1gpu-16vcpu-200gb \
  --preemptible \
  --container-port 8000 \
  --shm-size 16Gi \
  --disk-size 500Gi \
  --container-command bash \
  --args '-c vllm serve Qwen/Qwen-Image-Edit-2511 --omni --host 0.0.0.0 --port 8000'
```

## Security and credentials

The one-click URL leaves authentication off for the initial smoke test. Enable token authentication before production use. Supply endpoint tokens through `API_TOKEN` and optional Hugging Face credentials through `HF_TOKEN`; never commit either value or place it in a URL.

## Troubleshooting

- `502 failed to connect to local service`: weights are still loading and port 8000 is not ready. Poll `/v1/models` for JSON.
- `400` on edits: the endpoint expects multipart form fields named `image`, `prompt`, `model`, and optional generation fields—not JSON sent to `/v1/images/generations`.
- `401` or `403`: set `API_TOKEN` to the endpoint token.
- Out of memory: confirm the H100 preset and do not raise image size or concurrent requests before measuring memory.

## Cleanup

```bash
export ENDPOINT_ID='endpoint-...'
bash scripts/cleanup.sh
```

## Validation scope

Run `bash scripts/check.sh` for free local validation. The model is too large for this CPU-only repository test; final publication evidence must come from a paid Nebius H100 smoke run and its generated report.

## License and provenance

Project code and documentation are Apache-2.0. This project adapts a Nebius Serverless AI Cookbook template; details are in [ATTRIBUTION.md](ATTRIBUTION.md).
