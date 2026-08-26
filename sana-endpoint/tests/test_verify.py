import base64
import importlib.util
import pathlib
import unittest

SPEC = importlib.util.spec_from_file_location("verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_extract_png(self):
        png = b"\x89PNG\r\n\x1a\ncontent"
        self.assertEqual(VERIFY.extract_png({"data": [{"b64_json": base64.b64encode(png).decode()}]}), png)

    def test_bad_payload_fails(self):
        with self.assertRaises(ValueError):
            VERIFY.extract_png({"data": []})


if __name__ == "__main__":
    unittest.main()
