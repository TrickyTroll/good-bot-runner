import unittest
import runner.funcmodule as funcmodule

from pathlib import Path

CONFIGPATH = Path("./tests/examples")

class TestConfigTest(unittest.TestCase):
    """Testing that the config checker raises the right errors."""

    def test_raises_too_many_keys(self):
        too_many_keys = {
            "commands": ["ls", "echo 'foobar'"],
            "expect": ["prompt", "prompt"],
            "read": ["hello", "bye"],
        }
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

class TestNoInteractionChecker(unittest.TestCase):
    """Test for the check_parsed_config_no_interaction function."""
    def test_raises_wrong_type(self):
        """
        Passes a file that is seen as a list once unmarshalled.
        This test makes sure that the function will raise an error.
        See ``good-bot-runner/tests/examples/bad_conf_type.yaml``.
        """
        with self.assertRaises(TypeError):
            funcmodule.check_parsed_config_no_interaction(CONFIGPATH/ "bad_conf_type.yaml")
    def test_raises_too_many_keys(self):
        """
        This test makes sure that the function will raise an error
        when an unmarshalled configuration file contains too many
        keys.
        See ``good-bot-runner/tests/examples/bad_conf_keys.yaml``.
        """
        with self.assertRaises(KeyError):
            funcmodule.check_parsed_config_no_interaction(CONFIGPATH / "bad_conf_keys.yaml")
    def test_raises_bad_key_name(self):
        """
        Keys in a ``runner`` file can only be named ``commands``
        or ``expect``. If not, the checker should raise an error.
        See ``good-bot-runner/tests/examples/bad_conf_key_names.yaml``.
        """
        with self.assertRaises(KeyError):
            funcmodule.check_parsed_config_no_interaction(CONFIGPATH / "bad_conf_key_names.yaml")

if __name__ == "__main__":
    unittest.main()
