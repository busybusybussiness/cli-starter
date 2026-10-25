import io
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from cli_starter.cli import main  # noqa: E402
from cli_starter.config import ConfigError, load_config  # noqa: E402


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(argv)
    return code, buf.getvalue()


class ConfigTests(unittest.TestCase):
    def test_defaults_when_no_path(self):
        cfg = load_config(None)
        self.assertEqual(cfg.greeting, "Hello")
        self.assertFalse(cfg.loud)

    def test_missing_file_raises(self):
        with self.assertRaises(ConfigError):
            load_config("does-not-exist.toml")

    def test_invalid_types_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.toml")
            Path(p).write_text('loud = "yes"\n', encoding="utf-8")
            with self.assertRaises(ConfigError):
                load_config(p)

    def test_bad_toml_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.toml")
            Path(p).write_text("greeting = ", encoding="utf-8")
            with self.assertRaises(ConfigError):
                load_config(p)


class GreetTests(unittest.TestCase):
    def test_default_greeting(self):
        code, out = run(["greet", "--name", "Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "Hello, Ada!\n")

    def test_config_greeting_and_loud(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.toml")
            Path(p).write_text('greeting = "Howdy"\nloud = true\n', encoding="utf-8")
            code, out = run(["--config", p, "greet", "--name", "Ada"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "HOWDY, ADA!\n")

    def test_empty_name_is_error(self):
        code, out = run(["greet", "--name", "   "])
        self.assertEqual(code, 2)

    def test_bad_config_exit_code(self):
        code, _ = run(["--config", "nope.toml", "greet", "--name", "Ada"])
        self.assertEqual(code, 2)

    def test_version_flag(self):
        with self.assertRaises(SystemExit) as cm:
            run(["--version"])
        self.assertEqual(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
