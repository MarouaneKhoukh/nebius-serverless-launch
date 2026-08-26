import importlib.util
import pathlib
import unittest

SPEC = importlib.util.spec_from_file_location("verify", pathlib.Path(__file__).parents[1] / "scripts" / "verify.py")
VERIFY = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(VERIFY)


class VerifyTests(unittest.TestCase):
    def test_id3_is_audio(self):
        self.assertTrue(VERIFY.valid_audio(b"ID3content", "audio/mpeg"))

    def test_empty_is_not_audio(self):
        self.assertFalse(VERIFY.valid_audio(b"", "audio/mpeg"))


if __name__ == "__main__":
    unittest.main()
