import importlib.util
import pathlib
import sys
import types
import unittest

numpy = types.ModuleType("numpy")
numpy.ndarray = object
numpy.float32 = object()
numpy.asarray = lambda value, dtype=None: value
numpy.concatenate = lambda chunks: chunks
soundfile = types.ModuleType("soundfile")
soundfile.write = lambda *args, **kwargs: None
kokoro = types.ModuleType("kokoro")
kokoro.KPipeline = type("KPipeline", (), {})
sys.modules.setdefault("numpy", numpy)
sys.modules.setdefault("soundfile", soundfile)
sys.modules.setdefault("kokoro", kokoro)
SPEC = importlib.util.spec_from_file_location("kokoro_server", pathlib.Path(__file__).parents[1] / "serve.py")
SERVER = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(SERVER)


class ServerTests(unittest.TestCase):
    def test_voice_language_mapping(self):
        self.assertEqual(SERVER.lang_code_for_voice("af_bella"), "a")
        self.assertEqual(SERVER.lang_code_for_voice("bf_emma"), "b")
        self.assertEqual(SERVER.lang_code_for_voice("jf_alpha"), "j")

    def test_unknown_voice_uses_default(self):
        self.assertEqual(SERVER.lang_code_for_voice("unknown"), SERVER.DEFAULT_LANG)

    def test_empty_text_is_rejected(self):
        with self.assertRaises(Exception):
            SERVER.SpeechRequest(input="")


if __name__ == "__main__":
    unittest.main()
