import importlib.util
import json
import pathlib
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py"
)
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


def write_checkpoint(root: pathlib.Path, *, steps: int = 50) -> None:
    checkpoint = root / "checkpoints" / "last"
    model = checkpoint / "pretrained_model"
    model.mkdir(parents=True)
    (model / "model.safetensors").write_bytes(b"weights")
    (checkpoint / "train_config.json").write_text(
        json.dumps(
            {
                "steps": steps,
                "batch_size": 1,
                "seed": 42,
                "dataset": {
                    "repo_id": "lerobot/svla_so100_pickplace",
                    "revision": "728583b5eaf9e739a7f119e2def466fa1d552402",
                },
                "policy": {"type": "smolvla", "pretrained_path": "/tmp/smolvla-base"},
            }
        ),
        encoding="utf-8",
    )


class VerifyTests(unittest.TestCase):
    def test_valid_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            write_checkpoint(root)
            result = VERIFY.inspect_checkpoint(root)
            self.assertEqual(result["model_weight_bytes"], 7)
            self.assertEqual(result["observed_training_config"]["steps"], 50)

    def test_wrong_training_bound_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            write_checkpoint(root, steps=51)
            with self.assertRaisesRegex(ValueError, "steps"):
                VERIFY.inspect_checkpoint(root)

    def test_empty_weights_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            write_checkpoint(root)
            next(root.rglob("*.safetensors")).write_bytes(b"")
            with self.assertRaisesRegex(ValueError, "non-empty"):
                VERIFY.inspect_checkpoint(root)


if __name__ == "__main__":
    unittest.main()
