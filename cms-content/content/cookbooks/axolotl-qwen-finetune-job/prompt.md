Create a standalone Nebius AI GPU-job project that performs a bounded QLoRA fine-tune of Qwen2.5-0.5B with Axolotl.

Use `axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1`, one NVIDIA H100, a fixed random seed, a small public instruction dataset, and exactly 30 training steps. Supply a readable Axolotl YAML configuration and a reproducible Nebius job specification. Write output to local job storage during training, then copy the completed adapter to a mounted Object Storage bucket. Do not place cloud credentials in the repository.

The README must cover prerequisites, Nebius authentication, bucket creation, a least-privilege service account, IAM bindings, storage mounting, job submission, log monitoring, expected completion signals, artifact download, troubleshooting, current-price checking, and cleanup of the job, bucket data, and dedicated IAM bindings. Explain that the smoke run validates infrastructure and artifact production, not model quality.

Add an offline verifier that requires a parseable `adapter_config.json` and at least one non-empty `.safetensors` adapter file, checks expected base-model and LoRA fields, and emits a machine-readable JSON report. Add deterministic unit tests for configuration and artifact validation, plus credential-free CI. Keep the live Nebius smoke test opt-in and never invent cost, duration, or success evidence.
