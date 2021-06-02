import unittest
import runner.funcmodule as funcmodule

from pathlib import Path

CONFIGPATH = Path("./tests/examples")


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
