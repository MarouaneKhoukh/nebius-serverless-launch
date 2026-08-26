from pathlib import Path
import unittest

ROOT = Path(__file__).parents[1]
SCRIPT = (ROOT / "scripts" / "create_job.sh").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
COMMIT = "bf31dd794ffb4f87380aba3912f64421e8352d3c"
DATASET = "lerobot/svla_so100_pickplace"


class ContractTests(unittest.TestCase):
    def test_upstream_and_dataset_are_pinned_or_named(self):
        self.assertIn(COMMIT, SCRIPT)
        self.assertIn(COMMIT, README)
        self.assertIn(DATASET, SCRIPT)
        self.assertIn(DATASET, README)

    def test_training_is_bounded_and_secrets_absent(self):
        self.assertIn("--steps=50", SCRIPT)
        self.assertIn("--batch_size=1", SCRIPT)
        self.assertNotIn("AWS_SECRET_ACCESS_KEY", SCRIPT)


if __name__ == "__main__":
    unittest.main()
