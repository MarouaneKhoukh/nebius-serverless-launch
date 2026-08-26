import importlib.util
import pathlib
import unittest

SPEC = importlib.util.spec_from_file_location("verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_bearer_header_is_optional(self):
        self.assertEqual(VERIFY.request_headers(None), {})
        self.assertEqual(VERIFY.request_headers("secret")["Authorization"], "Bearer secret")

    def test_extract_reply(self):
        payload = {"choices": [{"message": {"content": " hello "}}]}
        self.assertEqual(VERIFY.extract_reply(payload), "hello")

    def test_empty_reply_fails(self):
        with self.assertRaises(ValueError):
            VERIFY.extract_reply({"choices": [{"message": {"content": ""}}]})


if __name__ == "__main__":
    unittest.main()
