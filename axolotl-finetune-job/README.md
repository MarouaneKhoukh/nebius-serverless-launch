# Fine-tune Qwen with Axolotl on Nebius Serverless Jobs

Run a bounded QLoRA smoke fine-tune of `Qwen/Qwen2.5-0.5B` with Axolotl in a Nebius Serverless GPU job. The configuration uses 30 training steps and persists adapter artifacts to a mounted Object Storage bucket.

[![Create job on Nebius](https://img.shields.io/badge/Create_job_on-Nebius-6C47FF?style=for-the-badge)](https://console.nebius.com/serverless/job/create?image=docker.io%2Faxolotlai%2Faxolotl%3Amain-20260309-py3.11-cu128-2.9.1&command=curl%20-fsSL%20https%3A%2F%2Fraw.githubusercontent.com%2FMarouaneKhoukh%2Fnebius-serverless-launch%2Fmain%2Faxolotl-finetune-job%2Fconfig.yaml%20-o%20%2Fworkspace%2Fdata%2Fconfig.yaml%20%26%26%20export%20RUN_ID%3Drun-%24%28date%20%2B%25Y%25m%25d-%25H%25M%25S%29%20%26%26%20axolotl%20train%20%2Fworkspace%2Fdata%2Fconfig.yaml%20%26%26%20mkdir%20-p%20%2Fworkspace%2Fdata%2Foutput%2F%24RUN_ID%20%26%26%20cp%20-r%20%2Fworkspace%2Foutput%2F.%20%2Fworkspace%2Fdata%2Foutput%2F%24RUN_ID&platform=gpu-h100-sxm&preset=1gpu-16vcpu-200gb&volume=%2Fworkspace%2Fdata&diskSize=500Gi&shmSize=16Gi&preemptible=true)

The form pre-fills the image, command, H100 preset, writable mount path, disk, shared memory, and preemptible capacity. You must select a project, networking, and an Object Storage bucket for `/workspace/data` before creating the job.

## Job contract

| Setting | Value |
| --- | --- |
| Base model | `Qwen/Qwen2.5-0.5B` |
| Method | QLoRA with rank 8 adapters |
| Dataset | `Salesforce/wikitext`, `wikitext-2-raw-v1`, first 2,000 training rows |
| Training budget | 30 steps, sequence length 128 |
| Image | `axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1` |
| Compute | `gpu-h100-sxm`, `1gpu-16vcpu-200gb` |
| Disk / shared memory | `500Gi` / `16Gi` |
| Output | `/workspace/data/output/run-YYYYmmdd-HHMMSS/` |

The base model and project are Apache-2.0. Dataset terms remain governed by the dataset publisher.

## CLI path

Create a bucket and get its resource ID, then submit the same job without putting storage credentials in the container:

```bash
nebius storage bucket create --name your-unique-axolotl-bucket
export BUCKET_ID="$(nebius storage bucket get-by-name --name your-unique-axolotl-bucket --format json | jq -r '.metadata.id')"
bash scripts/create_job.sh
```

The mounted bucket uses Nebius IAM. No `AWS_SECRET_ACCESS_KEY` is passed to the job command. `HF_TOKEN` is not required for the public default model; if you add one, use Nebius secret handling rather than committing it or placing it in a one-click URL.

## Verify the result

Watch the job and download its run folder:

```bash
nebius ai job logs JOB_ID --follow
aws s3 cp --recursive s3://YOUR_BUCKET/output/RUN_ID ./download/output
export ARTIFACT_DIR="$PWD/download/output"
export JOB_ID='job-...'
# Optional measured values from the Nebius job record/current pricing:
export JOB_RUNTIME_SECONDS='...'
export HOURLY_RATE_USD='...'
python3 scripts/verify.py
```

Verification requires `adapter_config.json` and at least one non-empty `.safetensors` file. It writes `run-report.json`; rates and runtimes are included only when you provide measured values.

[Nebius Academy: How to finetune a model using Nebius Serverless Jobs](https://www.youtube.com/watch?v=ZjD489E0lls) covers this job workflow.

## Why output is copied after training

Axolotl writes, replaces, and deletes files while training. An Object Storage mount is not a full POSIX filesystem, so `output_dir` stays on local job disk (`/workspace/output`). Only after successful training does the command copy the completed artifacts into the mounted bucket.

## Troubleshooting

- Permission errors under the bucket mount: keep `output_dir: /workspace/output`; do not train directly into `/workspace/data/output`.
- No artifacts: confirm the bucket is mounted writable at `/workspace/data` and inspect the final copy command in logs.
- Hub throttling: provide `HF_TOKEN` through Nebius secret management.
- Preempted job: resubmit or use regular capacity; this changes cost.

## Cleanup

```bash
export JOB_ID='job-...'
bash scripts/cleanup.sh
```

The cleanup script deletes only the job. Review and delete the Object Storage run artifacts separately after preserving evidence you need; bucket deletion is intentionally not automated.

Run `bash scripts/check.sh` for free local checks. Publishing as live-validated requires the paid GPU job and its measured report.

## License and provenance

Project code and documentation are Apache-2.0. See [ATTRIBUTION.md](ATTRIBUTION.md).
