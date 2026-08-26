from pathlib import Path
import unittest

CONFIG = (Path(__file__).parents[1] / "config.yaml").read_text(encoding="utf-8")


class ConfigTests(unittest.TestCase):
    def test_smoke_bounds_and_local_output(self):
        self.assertIn("base_model: Qwen/Qwen2.5-0.5B", CONFIG)
        self.assertIn("max_steps: 30", CONFIG)
        self.assertIn("output_dir: /workspace/output", CONFIG)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", CONFIG)


if __name__ == "__main__":
    unittest.main()
