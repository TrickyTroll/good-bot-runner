import unittest
import runner.funcmodule as funcmodule

from pathlib import Path

CONFIGPATH = Path("./tests/examples")

class TestConfigTest(unittest.TestCase):
    """Testing that the config checker raises the right errors."""
    def test_raises_too_many_keys(self):
        too_many_keys = {"commands": ["ls", "echo 'foobar'"],
                        "expect": ["prompt", "prompt"],
                        "read": ["hello", "bye"]}
        with self.assertRaises(KeyError):
            funcmodule.check_config(too_many_keys)
    def test_raises_bad_key(self):
        bad_key = {"commands": ["ls", "echo 'foobar'"], "read": ["hello", "bye"]}
        with self.assertRaises(KeyError):
            funcmodule.check_config(bad_key)

class TestParsing(unittest.TestCase):
    def test_returns_dict(self):
        """Testing that the function returns a `dict`."""

        result = funcmodule.parse_config(CONFIGPATH / "test_conf.yaml")

        self.assertEqual(type(result), type({}))

    def test_return_format(self):
        """Tests for the correct return format."""

        result = funcmodule.parse_config(CONFIGPATH / "test_conf.yaml")

        for keys, values in result.items():
            self.assertEqual(type(result), type({}))
            self.assertEqual(type(values), type([]))
            self.assertEqual(type(keys), type(""))


if __name__ == "__main__":
    unittest.main()
