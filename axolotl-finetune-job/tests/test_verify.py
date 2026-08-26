import importlib.util
import json
import pathlib
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_valid_adapter(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / "adapter_config.json").write_text(json.dumps({"base_model_name_or_path": "Qwen/Qwen2.5-0.5B"}))
            (root / "adapter_model.safetensors").write_bytes(b"weights")
            result = VERIFY.inspect_artifacts(root)
            self.assertEqual(result["weight_bytes"], 7)

    def test_missing_weights_fails(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
            VERIFY.inspect_artifacts(pathlib.Path(tmp))


if __name__ == "__main__":
    unittest.main()
