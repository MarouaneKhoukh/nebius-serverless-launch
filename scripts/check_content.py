#!/usr/bin/env python3
"""Offline structural checks for the staged Serverless CMS records."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COOKBOOKS = ROOT / "cms-content" / "content" / "cookbooks"

SOURCES = {
    "qwen3-serverless-endpoint": "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-vllm-qwen3-0-6b",
    "sana-serverless-endpoint": "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-sana",
    "kokoro-serverless-tts": "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-kokoro-82m",
    "qwen-image-edit-serverless": "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/endpoint-qwen-image-edit-2511",
    "axolotl-qwen-finetune-job": "https://github.com/nebius/serverless-ai-cookbook/tree/main/templates/job-axolotl-finetune",
    "smolvla-physical-ai-job": "https://github.com/MarouaneKhoukh/nebius-serverless-launch/tree/main/smolvla-finetune-job",
}

PLANNING_ESTIMATES = {
    "qwen3-serverless-endpoint": ("0.15", "10"),
    "sana-serverless-endpoint": ("0.20", "15"),
    "kokoro-serverless-tts": ("0.15", "10"),
    "qwen-image-edit-serverless": ("0.75", "20"),
    "axolotl-qwen-finetune-job": ("0.75", "20"),
    "smolvla-physical-ai-job": ("0.40", "30"),
}

REQUIRED_FRONTMATTER = {
    "id",
    "status",
    "slug",
    "category",
    "author",
    "model",
    "internal_content_description",
    "github_url",
    "video_url",
    "catalog_card_title",
    "catalog_card_description",
    "estimated_cost_per_run_usd",
    "cost_qualifier",
    "time_to_first_run_minutes",
    "time_qualifier",
    "metrics_verified_at",
    "published_at",
    "sort",
}


def frontmatter(text: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise AssertionError("index.md has no YAML frontmatter")
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            values[key.strip()] = value.strip().strip('"')
    return values


def main() -> None:
    actual = {path.name for path in COOKBOOKS.iterdir() if path.is_dir()}
    assert actual == set(SOURCES), f"unexpected cookbook directories: {sorted(actual ^ set(SOURCES))}"

    for slug, source in SOURCES.items():
        directory = COOKBOOKS / slug
        files = {path.name for path in directory.iterdir() if path.is_file()}
        assert files == {"index.md", "prompt.md", "eval.json"}, f"{slug}: wrong file set"

        index = (directory / "index.md").read_text(encoding="utf-8")
        prompt = (directory / "prompt.md").read_text(encoding="utf-8").strip()
        metadata = frontmatter(index)
        assert set(metadata) == REQUIRED_FRONTMATTER, f"{slug}: frontmatter keys differ"
        assert metadata["slug"] == slug
        assert metadata["status"] == "in_review"
        assert metadata["github_url"] == source
        expected_cost, expected_minutes = PLANNING_ESTIMATES[slug]
        assert metadata["estimated_cost_per_run_usd"] == expected_cost
        assert metadata["cost_qualifier"] == "approximate"
        assert metadata["time_to_first_run_minutes"] == expected_minutes
        assert metadata["time_qualifier"] == "approximately"
        assert metadata["metrics_verified_at"] == "null"
        assert metadata["published_at"] == "null"
        assert len(prompt) >= 40
        assert source in prompt
        assert not re.search(r"\b(?:TODO|TBD|N/A)\b", index + prompt)

        body = index.split("\n---\n", 1)[1]
        section_headings = re.findall(r"^## (.+)$", body, flags=re.MULTILINE)
        assert len(section_headings) == 5, f"{slug}: expected 5 recipe sections"
        assert section_headings[0] in {"What you'll build", "What you'll run"}
        assert section_headings[-1] == "Clean up and next steps"
        assert "> **Why this matters here:**" in body
        assert "```" in body, f"{slug}: missing runnable example"
        assert len(body.split()) >= 450, f"{slug}: recipe body is too shallow"
        assert re.search(r"\b[Ss]uccess", body), f"{slug}: missing success criteria"
        assert re.search(r"\b[Dd]elete\b", body), f"{slug}: missing cleanup instruction"
        assert "**Planning estimate:**" in body
        assert "metrics_verified_at` remains empty" in body

        evaluation = json.loads((directory / "eval.json").read_text(encoding="utf-8"))
        assert evaluation["enabled"] is False
        assert evaluation["execution"] is None
        assert evaluation["target"] is None
        assert evaluation["thresholds"] is None
        assert evaluation["checks"] == []

    removed = [
        "qwen3-endpoint",
        "sana-endpoint",
        "kokoro-tts-endpoint",
        "qwen-image-edit-endpoint",
        "axolotl-finetune-job",
    ]
    assert not any((ROOT / name).exists() for name in removed), "a duplicated runtime project remains"
    print("Validated 6 CMS records and confirmed 5 duplicated projects are absent.")


if __name__ == "__main__":
    main()
