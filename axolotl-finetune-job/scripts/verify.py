#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def inspect_artifacts(root: Path) -> dict[str, object]:
    configs = list(root.rglob("adapter_config.json"))
    weights = [path for path in root.rglob("*.safetensors") if path.stat().st_size > 0]
    if not configs:
        raise ValueError("adapter_config.json was not found")
    if not weights:
        raise ValueError("no non-empty .safetensors adapter weights were found")
    config = json.loads(configs[0].read_text(encoding="utf-8"))
    return {"adapter_config": str(configs[0]), "weight_files": [str(path) for path in weights], "weight_bytes": sum(path.stat().st_size for path in weights), "base_model_name_or_path": config.get("base_model_name_or_path")}


def main() -> None:
    artifact_dir = Path(os.environ["ARTIFACT_DIR"]).resolve()
    details = inspect_artifacts(artifact_dir)
    report: dict[str, object] = {"status": "passed", "kind": "serverless-job-artifact-check", "model": "Qwen/Qwen2.5-0.5B", "job_id": os.environ.get("JOB_ID"), "checked_at": datetime.now(timezone.utc).isoformat(), **details}
    runtime = os.environ.get("JOB_RUNTIME_SECONDS")
    rate = os.environ.get("HOURLY_RATE_USD")
    if runtime:
        report["job_runtime_seconds_supplied_by_operator"] = float(runtime)
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
    if runtime and rate:
        report["estimated_cost_usd"] = round(float(rate) * float(runtime) / 3600, 6)
    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("adapter artifacts verified; wrote run-report.json")


if __name__ == "__main__":
    main()
