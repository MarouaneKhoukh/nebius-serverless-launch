import importlib.util
import pathlib
import sys
import types
import unittest

torch = types.ModuleType("torch")
torch.float16 = object()
torch.bfloat16 = object()
torch.cuda = types.SimpleNamespace(is_available=lambda: False)
torch.Generator = object
diffusers = types.ModuleType("diffusers")
diffusers.SanaPipeline = type("SanaPipeline", (), {})
sys.modules.setdefault("torch", torch)
sys.modules.setdefault("diffusers", diffusers)
SPEC = importlib.util.spec_from_file_location("sana_server", pathlib.Path(__file__).parents[1] / "serve.py")
SERVER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(SERVER)


class ServerTests(unittest.TestCase):
    def test_default_and_valid_size(self):
        self.assertEqual(SERVER.parse_size(None), (1024, 1024))
        self.assertEqual(SERVER.parse_size("512x768"), (512, 768))

    def test_invalid_size_fails(self):
        for value in ("bad", "255x512", "513x512"):
            with self.subTest(value=value), self.assertRaises(SERVER.HTTPException):
                SERVER.parse_size(value)

    def test_request_limits_are_validated(self):
        with self.assertRaises(Exception):
            SERVER.GenerationRequest(prompt="")


if __name__ == "__main__":
    unittest.main()
