#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def headers(token: str | None, content: bool = False) -> dict[str, str]:
    result = {"Content-Type": "application/json"} if content else {}
    if token:
        result["Authorization"] = f"Bearer {token}"
    return result


def extract_png(payload: dict[str, object]) -> bytes:
    try:
        encoded = payload["data"][0]["b64_json"]  # type: ignore[index]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("response is missing data[0].b64_json") from exc
    png = base64.b64decode(encoded, validate=True) if isinstance(encoded, str) else b""
    if not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("response did not contain a PNG")
    return png


def main() -> None:
    base = os.environ["BASE_URL"].rstrip("/")
    token = os.environ.get("API_TOKEN")
    started_wall = datetime.now(timezone.utc)
    started = time.monotonic()
    for attempt in range(60):
        try:
            req = urllib.request.Request(f"{base}/v1/models", headers=headers(token))
            with urllib.request.urlopen(req, timeout=30) as response:
                if json.load(response).get("data"):
                    break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
        if attempt == 59:
            raise SystemExit("timed out after 15 minutes waiting for /v1/models")
        print("waiting for /v1/models...", flush=True)
        time.sleep(15)
    body = json.dumps({"prompt": "a red fox in a snowy pine forest at golden hour", "size": "1024x1024", "seed": 42}).encode()
    req = urllib.request.Request(f"{base}/v1/images/generations", data=body, headers=headers(token, True), method="POST")
    with urllib.request.urlopen(req, timeout=600) as response:
        png = extract_png(json.load(response))
    Path("sana.png").write_bytes(png)
    elapsed = round(time.monotonic() - started, 3)
    report: dict[str, object] = {"status": "passed", "kind": "serverless-endpoint-smoke-test", "model": "Efficient-Large-Model/Sana_1600M_1024px_diffusers", "started_at": started_wall.isoformat(), "elapsed_seconds_including_readiness_wait": elapsed, "output": "sana.png", "output_bytes": len(png)}
    rate = os.environ.get("HOURLY_RATE_USD")
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
        report["estimated_cost_usd_for_elapsed_time"] = round(float(rate) * elapsed / 3600, 6)
    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("wrote sana.png and run-report.json")


if __name__ == "__main__":
    main()
