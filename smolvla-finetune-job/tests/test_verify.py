import importlib.util
import pathlib
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_valid_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            final = pathlib.Path(tmp) / "checkpoints" / "last" / "pretrained_model"
            final.mkdir(parents=True)
            (final / "config.json").write_text("{}")
            (final / "model.safetensors").write_bytes(b"weights")
            result = VERIFY.inspect_checkpoint(pathlib.Path(tmp))
            self.assertEqual(result["model_weight_bytes"], 7)

    def test_weights_without_config_are_not_enough(self):
        with tempfile.TemporaryDirectory() as tmp:
            final = pathlib.Path(tmp)
            (final / "model.safetensors").write_bytes(b"weights")
            with self.assertRaises(ValueError):
                VERIFY.inspect_checkpoint(pathlib.Path(tmp))


if __name__ == "__main__":
    unittest.main()
