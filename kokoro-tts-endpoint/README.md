# Kokoro-82M TTS on Nebius Serverless

Deploy `hexgrad/Kokoro-82M` behind an OpenAI-shaped speech API on one preemptible Nebius L40S GPU. The API accepts text and returns MP3 or WAV audio.

[![Deploy on Nebius](https://img.shields.io/badge/Deploy_on-Nebius-6C47FF?style=for-the-badge)](https://console.nebius.com/serverless/endpoint/create?image=cr.eu-north1.nebius.cloud%2Fe00gw2b7v3pxetvpy7%2Fkokoro-serve%3Ad315ae1&targetPort=8000&platform=gpu-l40s-a&preset=1gpu-8vcpu-32gb&diskSize=500Gi&shmSize=16Gi&preemptible=true)

The link uses the tested immutable cookbook image tag. Select your Nebius project and networking, review the pre-filled configuration, and create the endpoint. To control the supply chain yourself, build the included `Dockerfile` and substitute your registry image.

## Deployment contract

| Setting | Value |
| --- | --- |
| Model | `hexgrad/Kokoro-82M` |
| API | `POST /v1/audio/speech` |
| Published image | `cr.eu-north1.nebius.cloud/e00gw2b7v3pxetvpy7/kokoro-serve:d315ae1` |
| Compute | `gpu-l40s-a`, `1gpu-8vcpu-32gb` |
| Port | `8000` |
| Disk / shared memory | `500Gi` / `16Gi` |
| Capacity | preemptible |

Model source and license: [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) (Apache-2.0). The image provides English G2P; default voice is `af_bella`.

## Build your own image

```bash
docker build -t your-registry.example/kokoro-serve:1 .
docker push your-registry.example/kokoro-serve:1
```

Optional overrides: `MODEL_ID`, `DEFAULT_VOICE`, `LANG_CODE`, and `PORT`.

## Verify the result

```bash
export BASE_URL='https://your-endpoint.example'
export API_TOKEN='your-endpoint-token' # only when auth is enabled
python3 scripts/verify.py
```

The script waits for readiness, generates a short deterministic utterance, validates the audio container, and writes `kokoro-sample.mp3` plus `run-report.json`. If you supply a current `HOURLY_RATE_USD`, the report includes an estimate based on measured elapsed time.

The general deployment flow is covered by [Nebius Academy: How to deploy a Model using Nebius Serverless endpoints](https://www.youtube.com/watch?v=Ftr-6JF08ZI). It is not a Kokoro-specific demo.

## CLI alternative

```bash
nebius ai endpoint create \
  --image cr.eu-north1.nebius.cloud/e00gw2b7v3pxetvpy7/kokoro-serve:d315ae1 \
  --public \
  --platform gpu-l40s-a \
  --preset 1gpu-8vcpu-32gb \
  --preemptible \
  --container-port 8000 \
  --shm-size 16Gi \
  --disk-size 500Gi
```

## Security

The one-click URL leaves authentication off for the initial test. Enable endpoint token authentication for production, pass the token through `API_TOKEN`, and keep any optional `HF_TOKEN` in a secret/environment variable. Request speed is bounded to 0.25–4.0; add application-level text-length and rate limits for public production use.

## Troubleshooting

- `502 failed to connect to local service`: wait for the model and G2P pipeline to load; poll `/v1/models`.
- Empty or invalid MP3: inspect endpoint logs for `ffmpeg`; the Dockerfile installs it explicitly.
- Voice error: choose a voice from the model's [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md).
- `401` or `403`: set `API_TOKEN` to the configured endpoint token.

## Cleanup

```bash
export ENDPOINT_ID='endpoint-...'
bash scripts/cleanup.sh
```

Run `bash scripts/check.sh` for free local checks. A paid GPU smoke run and its generated report are required before claiming live validation in the CMS.

## License and provenance

Project code and documentation are Apache-2.0. See [ATTRIBUTION.md](ATTRIBUTION.md).
