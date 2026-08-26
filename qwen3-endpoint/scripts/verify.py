#!/usr/bin/env python3
"""Wait for Qwen3, make one request, and record reproducible evidence."""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "Qwen/Qwen3-0.6B"


def request_headers(token: str | None, json_body: bool = False) -> dict[str, str]:
    headers = {"Content-Type": "application/json"} if json_body else {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def extract_reply(payload: dict[str, object]) -> str:
    try:
        reply = payload["choices"][0]["message"]["content"]  # type: ignore[index]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("response is missing choices[0].message.content") from exc
    if not isinstance(reply, str) or not reply.strip():
        raise ValueError("model returned empty text")
    return reply.strip()


def get_json(url: str, headers: dict[str, str], timeout: int) -> dict[str, object]:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)


def main() -> None:
    base_url = os.environ["BASE_URL"].rstrip("/")
    token = os.environ.get("API_TOKEN")
    started_wall = datetime.now(timezone.utc)
    started = time.monotonic()

    for attempt in range(60):
        try:
            models = get_json(f"{base_url}/v1/models", request_headers(token), 30)
            if models.get("data"):
                break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
        if attempt == 59:
            raise SystemExit("timed out after 15 minutes waiting for /v1/models")
        print("waiting for /v1/models...", flush=True)
        time.sleep(15)

    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": "Say hello in one short sentence."}],
        "max_tokens": 64,
        "temperature": 0.2,
    }).encode()
    req = urllib.request.Request(
        f"{base_url}/v1/chat/completions",
        data=body,
        headers=request_headers(token, json_body=True),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        payload = json.load(response)
    reply = extract_reply(payload)
    elapsed = round(time.monotonic() - started, 3)
    Path("reply.txt").write_text(reply + "\n", encoding="utf-8")
    report: dict[str, object] = {
        "status": "passed",
        "kind": "serverless-endpoint-smoke-test",
        "model": MODEL,
        "started_at": started_wall.isoformat(),
        "elapsed_seconds_including_readiness_wait": elapsed,
        "output": "reply.txt",
        "output_characters": len(reply),
    }
    rate = os.environ.get("HOURLY_RATE_USD")
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
        report["estimated_cost_usd_for_elapsed_time"] = round(float(rate) * elapsed / 3600, 6)
    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(reply)
    print("wrote reply.txt and run-report.json")


if __name__ == "__main__":
    main()
