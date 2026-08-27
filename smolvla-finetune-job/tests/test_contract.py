from pathlib import Path
from html import unescape
import re
import unittest
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).parents[1]
SCRIPT = (ROOT / "scripts" / "create_job.sh").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")

IMAGE_DIGEST = "sha256:bfb0ea7cbd47c536f2bd46d885d0b4b2e2750d9f1da2f92cc5a69cc095eaa6a7"
MODEL_REVISION = "c83c3163b8ca9b7e67c509fffd9121e66cb96205"
DATASET_REVISION = "728583b5eaf9e739a7f119e2def466fa1d552402"


class ContractTests(unittest.TestCase):
    def test_runtime_inputs_are_pinned(self):
        for value in (IMAGE_DIGEST, MODEL_REVISION, DATASET_REVISION):
            self.assertIn(value, SCRIPT)
            self.assertIn(value, README)

    def test_training_is_bounded(self):
        for value in (
            "--policy.path=/tmp/smolvla-base",
            "--policy.empty_cameras=1",
            "--dataset.repo_id=lerobot/svla_so100_pickplace",
            "observation.images.top",
            "observation.images.wrist",
            "--batch_size=1",
            "--steps=50",
            "--seed=42",
            "--policy.device=cuda",
            "--policy.push_to_hub=false",
        ):
            self.assertIn(value, SCRIPT)

    def test_job_has_guardrails_and_persistent_output(self):
        for value in ("--timeout 1h", "SMOLVLA_PREEMPTIBLE", "/tmp/output:rw", "BUCKET_ID", "SUBNET_ID"):
            self.assertIn(value, SCRIPT)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", SCRIPT)
        self.assertNotIn("HF_TOKEN=", SCRIPT)

    def test_one_click_link_matches_the_job_contract(self):
        match = re.search(
            r'<a href="(https://console\.nebius\.com/serverless/job/create\?[^"]+)"', README
        )
        self.assertIsNotNone(match)
        query = parse_qs(urlparse(unescape(match.group(1))).query)
        self.assertEqual(
            query["image"],
            [f"marouanekhoukh/smolvla-nebius@{IMAGE_DIGEST}"],
        )
        self.assertEqual(query["platform"], ["gpu-h100-sxm"])
        self.assertEqual(query["preset"], ["1gpu-16vcpu-200gb"])
        self.assertEqual(query["volume"], ["/tmp/output"])
        for value in (MODEL_REVISION, DATASET_REVISION, "--steps=50", "--batch_size=1"):
            self.assertIn(value, query["command"][0])


if __name__ == "__main__":
    unittest.main()
