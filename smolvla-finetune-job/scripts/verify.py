#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def inspect_checkpoint(root: Path) -> dict[str, object]:
    weights = [path for path in root.rglob("*.safetensors") if path.stat().st_size > 0]
    if not weights:
        raise ValueError("checkpoint has no non-empty .safetensors model file")
    configs = [
        path
        for path in root.rglob("*.json")
        if path.name in {"train_config.json", "config.json", "policy_preprocessor.json"}
    ]
    if not configs:
        raise ValueError("checkpoint has no saved LeRobot training/model configuration")
    return {
        "checkpoint_root": str(root),
        "config_files": [str(path) for path in configs],
        "model_weight_files": [str(path) for path in weights],
        "model_weight_bytes": sum(path.stat().st_size for path in weights),
    }


def main() -> None:
    root = Path(os.environ["ARTIFACT_DIR"]).resolve()
    details = inspect_checkpoint(root)
    report: dict[str, object] = {"status": "passed", "kind": "serverless-physical-ai-job-artifact-check", "model": "lerobot/smolvla_base", "dataset": "lerobot/svla_so100_pickplace", "upstream_commit": "bf31dd794ffb4f87380aba3912f64421e8352d3c", "training_steps": 50, "job_id": os.environ.get("JOB_ID"), "checked_at": datetime.now(timezone.utc).isoformat(), **details}
    runtime = os.environ.get("JOB_RUNTIME_SECONDS")
    rate = os.environ.get("HOURLY_RATE_USD")
    if runtime:
        report["job_runtime_seconds_supplied_by_operator"] = float(runtime)
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
    if runtime and rate:
        report["estimated_cost_usd"] = round(float(rate) * float(runtime) / 3600, 6)
    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("SmolVLA checkpoint verified; wrote run-report.json")


if __name__ == "__main__":
    main()
