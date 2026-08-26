import base64
import importlib.util
import pathlib
import unittest

SPEC = importlib.util.spec_from_file_location("verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_ppm_has_expected_header(self):
        self.assertTrue(VERIFY.make_ppm(4, 3).startswith(b"P6\n4 3\n255\n"))

    def test_multipart_contains_fields_and_file(self):
        body, boundary = VERIFY.multipart({"prompt": "sunset"}, "input.ppm", b"P6")
        self.assertIn(boundary.encode(), body)
        self.assertIn(b'name="prompt"', body)
        self.assertIn(b'filename="input.ppm"', body)

    def test_extract_png(self):
        png = b"\x89PNG\r\n\x1a\nrest"
        payload = {"data": [{"b64_json": base64.b64encode(png).decode()}]}
        self.assertEqual(VERIFY.extract_png(payload), png)


if __name__ == "__main__":
    unittest.main()
