# Sana text-to-image on Nebius Serverless

Deploy `Efficient-Large-Model/Sana_1600M_1024px_diffusers` behind an OpenAI-shaped image generation API on one preemptible Nebius L40S GPU.

[![Deploy on Nebius](https://img.shields.io/badge/Deploy_on-Nebius-6C47FF?style=for-the-badge)](https://console.nebius.com/serverless/endpoint/create?image=cr.eu-north1.nebius.cloud%2Fe00gw2b7v3pxetvpy7%2Fsana-serve%3Ad315ae1&targetPort=8000&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

The button uses the tested immutable cookbook image tag. You can also build `Dockerfile` and publish it to a registry you control. In the Nebius console, select your project and networking, review the pre-filled configuration, and create the endpoint.

## Deployment contract

| Setting | Value |
| --- | --- |
| Model | `Efficient-Large-Model/Sana_1600M_1024px_diffusers` |
| API | `POST /v1/images/generations` |
| Published image | `cr.eu-north1.nebius.cloud/e00gw2b7v3pxetvpy7/sana-serve:d315ae1` |
| Compute | `gpu-l40s-a`, `1gpu-8vcpu-32gb` |
| Port | `8000` |
| Disk / shared memory | `500Gi` / `16Gi` |
| Capacity | preemptible |

The default model is Apache-2.0. Its [model card](https://huggingface.co/Efficient-Large-Model/Sana_1600M_1024px_diffusers) is the source of truth. Changing `MODEL_ID` may change the applicable license.

## Build your own image

```bash
docker build -t your-registry.example/sana-serve:1 .
docker push your-registry.example/sana-serve:1
```

The server defaults are complete, so no environment variables are required for the one-click path. Supported overrides are `MODEL_ID`, `MODEL_VARIANT`, `IMAGE_SIZE`, `INFERENCE_STEPS`, `GUIDANCE_SCALE`, `MAX_IMAGES`, `MAX_STEPS`, and `MAX_SIDE`.

## Verify the result

```bash
export BASE_URL='https://your-endpoint.example'
export API_TOKEN='your-endpoint-token' # only when auth is enabled
python3 scripts/verify.py
```

The script waits for model readiness, requests a seeded 1024×1024 image, validates the PNG, and writes `sana.png` plus `run-report.json`. Supply a current `HOURLY_RATE_USD` to calculate an estimate from observed elapsed time.

The general deployment flow appears in [Nebius Academy: How to deploy a Model using Nebius Serverless endpoints](https://www.youtube.com/watch?v=Ftr-6JF08ZI); it is a platform walkthrough, not a Sana-specific demo.

## CLI alternative

```bash
nebius ai endpoint create \
  --image cr.eu-north1.nebius.cloud/e00gw2b7v3pxetvpy7/sana-serve:d315ae1 \
  --public \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --preemptible \
  --container-port 8000 \
  --shm-size 16Gi \
  --disk-size 500Gi
```

## Security

Authentication is off in the one-click URL for the first smoke test. Enable token authentication for production. Pass endpoint credentials with `API_TOKEN` and optional Hub credentials with `HF_TOKEN`; do not commit them or place them in URLs. The API limits image count, dimensions, and inference steps to reduce accidental GPU abuse.

## Troubleshooting

- `502 failed to connect to local service`: model loading is incomplete; poll `/v1/models` until it returns JSON.
- `no CUDA device`: the endpoint was created on a CPU preset.
- Black output: keep the text encoder and VAE in bf16; `serve.py` already applies this published Sana requirement.
- `400` for size: both sides must be 256–2048 and divisible by 32.

## Cleanup

```bash
export ENDPOINT_ID='endpoint-...'
bash scripts/cleanup.sh
```

Run `bash scripts/check.sh` for free local checks. Final CMS evidence requires a paid GPU smoke run and the generated report.

## License and provenance

Project code and documentation are Apache-2.0. See [ATTRIBUTION.md](ATTRIBUTION.md).
