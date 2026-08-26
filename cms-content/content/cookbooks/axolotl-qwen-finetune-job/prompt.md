Build a standalone Nebius GPU-job project that runs a bounded QLoRA fine-tune of Qwen2.5-0.5B with Axolotl. Deliver `config.yaml`, job creation, verification, cleanup, and check scripts, a complete `README.md`, deterministic tests, and GitHub Actions.

Use `axolotlai/axolotl:main-20260309-py3.11-cu128-2.9.1`, one H100, a fixed seed, a small public instruction dataset, and exactly 30 training steps. Write output locally during training, then copy the completed adapter to mounted Object Storage.

Document authentication, a least-privilege service account, bucket and mount setup, job submission, logs, artifact download, troubleshooting, price checking, and cleanup. The offline verifier must require a valid `adapter_config.json` and a non-empty `.safetensors` adapter, validate base-model and LoRA fields, and write a JSON report. Keep local tests credential- and GPU-free, make live execution opt-in, and never fabricate quality, cost, duration, or success evidence.
