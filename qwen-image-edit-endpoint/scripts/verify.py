#!/usr/bin/env python3
"""Smoke-test Qwen Image Edit and write an evidence report."""

from __future__ import annotations

import base64
import json
import os
import secrets
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "Qwen/Qwen-Image-Edit-2511"


def auth_headers(token: str | None) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"} if token else {}


def make_ppm(width: int = 512, height: int = 512) -> bytes:
    """Create a simple sky/ground image without third-party libraries."""
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            if y < height * 2 // 3:
                pixels.extend((80 + x * 60 // width, 150, 220))
            else:
                pixels.extend((45, 105 + x * 25 // width, 55))
    return f"P6\n{width} {height}\n255\n".encode() + bytes(pixels)


def multipart(fields: dict[str, str], filename: str, file_bytes: bytes) -> tuple[bytes, str]:
    boundary = "----codex-" + secrets.token_hex(12)
    chunks: list[bytes] = []
    for key, value in fields.items():
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
            value.encode(),
            b"\r\n",
        ])
    chunks.extend([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'.encode(),
        b"Content-Type: image/x-portable-pixmap\r\n\r\n",
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return b"".join(chunks), boundary


def extract_png(payload: dict[str, object]) -> bytes:
    try:
        encoded = payload["data"][0]["b64_json"]  # type: ignore[index]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("response is missing data[0].b64_json") from exc
    if not isinstance(encoded, str):
        raise ValueError("b64_json is not a string")
    png = base64.b64decode(encoded, validate=True)
    if not png.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("decoded response is not a PNG")
    return png


def main() -> None:
    base_url = os.environ["BASE_URL"].rstrip("/")
    token = os.environ.get("API_TOKEN")
    started_wall = datetime.now(timezone.utc)
    started = time.monotonic()
    for attempt in range(60):
        try:
            req = urllib.request.Request(f"{base_url}/v1/models", headers=auth_headers(token))
            with urllib.request.urlopen(req, timeout=30) as response:
                if json.load(response).get("data"):
                    break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            pass
        if attempt == 59:
            raise SystemExit("timed out after 15 minutes waiting for /v1/models")
        print("waiting for /v1/models...", flush=True)
        time.sleep(15)

    source = make_ppm()
    Path("qwen-edit-input.ppm").write_bytes(source)
    body, boundary = multipart(
        {"model": MODEL, "prompt": "make the sky a dramatic sunset", "size": "1024x1024", "output_format": "png", "num_inference_steps": "20", "seed": "42"},
        "qwen-edit-input.ppm",
        source,
    )
    headers = auth_headers(token)
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    req = urllib.request.Request(f"{base_url}/v1/images/edits", data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=600) as response:
        payload = json.load(response)
    png = extract_png(payload)
    Path("qwen-edit.png").write_bytes(png)
    elapsed = round(time.monotonic() - started, 3)
    report: dict[str, object] = {
        "status": "passed",
        "kind": "serverless-endpoint-smoke-test",
        "model": MODEL,
        "started_at": started_wall.isoformat(),
        "elapsed_seconds_including_readiness_wait": elapsed,
        "input": "qwen-edit-input.ppm",
        "output": "qwen-edit.png",
        "output_bytes": len(png),
    }
    rate = os.environ.get("HOURLY_RATE_USD")
    if rate:
        report["hourly_rate_usd_supplied_by_operator"] = float(rate)
        report["estimated_cost_usd_for_elapsed_time"] = round(float(rate) * elapsed / 3600, 6)
    Path("run-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("wrote qwen-edit.png and run-report.json")


if __name__ == "__main__":
    main()
