#!/usr/bin/env python3
"""Validate a downloaded SmolVLA smoke-run checkpoint."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

MODEL = "lerobot/smolvla_base"
MODEL_REVISION = "c83c3163b8ca9b7e67c509fffd9121e66cb96205"
DATASET = "lerobot/svla_so100_pickplace"
DATASET_REVISION = "728583b5eaf9e739a7f119e2def466fa1d552402"
STEPS = 50
BATCH_SIZE = 1
SEED = 42


def relative_paths(paths: list[Path], root: Path) -> list[str]:
    return [str(path.relative_to(root)) for path in sorted(paths)]


def inspect_checkpoint(root: Path) -> dict[str, object]:
    if not root.is_dir():
        raise ValueError(f"artifact directory does not exist: {root}")

    weights = [path for path in root.rglob("*.safetensors") if path.stat().st_size > 0]
    if not weights:
        raise ValueError("checkpoint has no non-empty .safetensors model file")

    configs = sorted(root.rglob("train_config.json"))
    if not configs:
        raise ValueError("checkpoint has no train_config.json")

    config_path = configs[-1]
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {config_path}") from exc

    dataset = config.get("dataset")
    policy = config.get("policy")
    if not isinstance(dataset, dict) or not isinstance(policy, dict):
        raise ValueError("train_config.json is missing dataset or policy configuration")

    expected = {
        "steps": STEPS,
        "batch_size": BATCH_SIZE,
        "seed": SEED,
        "dataset.repo_id": DATASET,
        "dataset.revision": DATASET_REVISION,
    }
    observed = {
        "steps": config.get("steps"),
        "batch_size": config.get("batch_size"),
        "seed": config.get("seed"),
        "dataset.repo_id": dataset.get("repo_id"),
        "dataset.revision": dataset.get("revision"),
    }
    for key, value in expected.items():
        if observed[key] != value:
            raise ValueError(f"{key} is {observed[key]!r}, expected {value!r}")

    policy_type = policy.get("type")
    if policy_type != "smolvla":
        raise ValueError(f"policy.type is {policy_type!r}, expected 'smolvla'")

    return {
        "checkpoint_root": str(root),
        "train_config": str(config_path.relative_to(root)),
        "model_weight_files": relative_paths(weights, root),
        "model_weight_bytes": sum(path.stat().st_size for path in weights),
        "observed_training_config": {**observed, "policy.type": policy_type},
    }


def main() -> None:
    root = Path(os.environ["ARTIFACT_DIR"]).expanduser().resolve()
    details = inspect_checkpoint(root)
    report: dict[str, object] = {
        "status": "passed",
        "kind": "serverless-smolvla-job-artifact-check",
        "model": MODEL,
        "model_revision_requested": MODEL_REVISION,
        "dataset": DATASET,
        "dataset_revision": DATASET_REVISION,
        "job_id": os.environ.get("JOB_ID"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        **details,
    }

    runtime = os.environ.get("JOB_RUNTIME_SECONDS")
    rate = os.environ.get("HOURLY_RATE_USD")
    if runtime:
        report["job_runtime_seconds_supplied_by_operator"] = float(runtime)
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
    if runtime and rate:
        report["estimated_cost_usd_from_supplied_values"] = round(float(rate) * float(runtime) / 3600, 6)

    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("SmolVLA checkpoint verified; wrote run-report.json")


if __name__ == "__main__":
    main()
