#!/usr/bin/env python3
from __future__ import annotations

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


def valid_audio(payload: bytes, media_type: str) -> bool:
    return bool(payload) and (payload.startswith(b"ID3") or payload[:2] in {b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"} or (media_type.startswith("audio/") and len(payload) > 1024))


def main() -> None:
    base = os.environ["BASE_URL"].rstrip("/")
    token = os.environ.get("API_TOKEN")
    started_wall = datetime.now(timezone.utc)
    started = time.monotonic()
    for attempt in range(40):
        try:
            req = urllib.request.Request(f"{base}/v1/models", headers=headers(token))
            with urllib.request.urlopen(req, timeout=30) as response:
                if json.load(response).get("data"):
                    break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
        if attempt == 39:
            raise SystemExit("timed out after 10 minutes waiting for /v1/models")
        print("waiting for /v1/models...", flush=True)
        time.sleep(15)
    body = json.dumps({"model": "kokoro", "input": "Hello from Kokoro on Nebius Serverless.", "voice": "af_bella", "response_format": "mp3", "speed": 1.0}).encode()
    req = urllib.request.Request(f"{base}/v1/audio/speech", data=body, headers=headers(token, True), method="POST")
    with urllib.request.urlopen(req, timeout=180) as response:
        media_type = response.headers.get("Content-Type", "")
        audio = response.read()
    if not valid_audio(audio, media_type):
        raise ValueError("endpoint response is not recognizable non-empty audio")
    Path("kokoro-sample.mp3").write_bytes(audio)
    elapsed = round(time.monotonic() - started, 3)
    report: dict[str, object] = {"status": "passed", "kind": "serverless-endpoint-smoke-test", "model": "hexgrad/Kokoro-82M", "started_at": started_wall.isoformat(), "elapsed_seconds_including_readiness_wait": elapsed, "output": "kokoro-sample.mp3", "output_bytes": len(audio), "content_type": media_type}
    rate = os.environ.get("HOURLY_RATE_USD")
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
        report["estimated_cost_usd_for_elapsed_time"] = round(float(rate) * elapsed / 3600, 6)
    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("wrote kokoro-sample.mp3 and run-report.json")


if __name__ == "__main__":
    main()
