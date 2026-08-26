# Nebius Serverless launch projects

Six self-contained, one-click examples for a Nebius Serverless AI launch: four inference endpoints and two GPU fine-tuning jobs.

| Project | Type | Compute | Walkthrough |
| --- | --- | --- | --- |
| [Qwen3-0.6B](qwen3-endpoint/) | OpenAI-compatible chat endpoint | L40S | [Deploy video](https://www.youtube.com/watch?v=Ftr-6JF08ZI) |
| [Sana](sana-endpoint/) | Text-to-image endpoint | L40S | [Deploy video](https://www.youtube.com/watch?v=Ftr-6JF08ZI) |
| [Kokoro-82M](kokoro-tts-endpoint/) | Text-to-speech endpoint | L40S | [Deploy video](https://www.youtube.com/watch?v=Ftr-6JF08ZI) |
| [Qwen Image Edit](qwen-image-edit-endpoint/) | Image-edit endpoint | H100 | [Deploy video](https://www.youtube.com/watch?v=Ftr-6JF08ZI) |
| [Axolotl + Qwen2.5](axolotl-finetune-job/) | QLoRA fine-tuning job | H100 | [Fine-tune video](https://www.youtube.com/watch?v=ZjD489E0lls) |
| [SmolVLA](smolvla-finetune-job/) | Physical-AI fine-tuning job | L40S | [Fine-tune video](https://www.youtube.com/watch?v=ZjD489E0lls) |

Each folder is independently documented and includes:

- a pre-filled Nebius console launch link and CLI alternative;
- pinned models, images, or upstream source revisions;
- a bounded smoke test with explicit success criteria;
- a machine-readable evidence report without invented cost or runtime figures;
- environment-variable or managed-secret credential handling;
- troubleshooting, cleanup, licensing, and attribution;
- local tests run by the repository-level CI workflow.

## Validate everything locally

```bash
for project in \
  qwen3-endpoint \
  sana-endpoint \
  kokoro-tts-endpoint \
  qwen-image-edit-endpoint \
  axolotl-finetune-job \
  smolvla-finetune-job
do
  (cd "$project" && bash scripts/check.sh)
done
```

These checks do not allocate Nebius resources. A live endpoint or training job consumes paid GPU capacity; run the project-specific verifier afterward and keep its `run-report.json` as publication evidence.

## CMS links

Each catalog item can use its folder URL as `github_url`, for example:

```text
https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/qwen3-endpoint
```

This preserves one reviewable repository while keeping every launch item addressable as a distinct project.

## License

Repository-authored code and documentation are Apache-2.0. Each project folder includes precise upstream attribution. Models, datasets, and external source code retain their upstream licenses.
