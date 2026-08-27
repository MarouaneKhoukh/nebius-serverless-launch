# Nebius Serverless launch content

This repository stages six Serverless AI cookbook records for the Nebius developer-hub CMS. It does not duplicate Serverless examples that already exist.

| CMS recipe | Runtime source |
| --- | --- |
| Qwen3-0.6B endpoint | [Official Serverless template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-vllm-qwen3-0-6b) |
| Sana endpoint | [Official Serverless template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-sana) |
| Kokoro-82M endpoint | [Official Serverless template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-kokoro-82m) |
| Qwen Image Edit endpoint | [Official Serverless template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-qwen-image-edit-2511) |
| Axolotl fine-tuning job | [Official Serverless template](https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/job-axolotl-finetune) |
| SmolVLA physical-AI job | [New template in this repository](smolvla-finetune-job/) |

The five existing recipes contribute only the CMS source required by Daniel's manifest repository: `index.md`, `prompt.md`, and `eval.json`. The prompt tells a coding agent to set up and run the linked recipe; it does not ask the agent to recreate that recipe.

SmolVLA is the only new runtime example. It adapts the existing physical-AI material into a one-click Nebius Serverless Job using a minimal root wrapper around Hugging Face's pinned GPU image, plus the pinned model, dataset, and LeRobot training command.

## Repository layout

```text
cms-content/              Six CMS source records plus author/category references
smolvla-finetune-job/     New one-click physical-AI Serverless Job template
scripts/check_content.py  Free, offline content validation
```

## Validate locally

```bash
python3 scripts/check_content.py
(cd smolvla-finetune-job && bash scripts/check.sh)
```

These checks use no credentials, network, GPU, or paid Nebius resources. All six entries remain `in_review`. Cost and time figures are clearly labeled editorial planning estimates; `metrics_verified_at` stays empty until controlled live runs establish evidence.

## Cost units

Endpoints are estimated per active hour, while Serverless Jobs are estimated per run. Daniel's current CMS schema only has `estimated_cost_per_run_usd`, so the four endpoint records leave that structured field empty and state their hourly estimates in the catalog descriptions and recipe bodies. The CMS should eventually add an explicit `cost_unit` such as `hour` or `run` before hourly endpoint figures are placed in the dedicated cost metric.

## License

Repository-authored material is Apache-2.0. Linked templates, models, datasets, images, and upstream code retain their respective licenses.
