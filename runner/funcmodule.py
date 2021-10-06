# -*- coding: utf-8 -*-
"""Functions used by the `runner` program.

This module contains the function used by `runner` to parse
configuration files.

## Example

To parse a config, you can simply::

```python
import funcmodule
parsed = funcmodule.parse_config(conf)
```
    
`parsed` will be a `dict` representation of a `yaml`
text file.
"""

import pathlib
import sys
import yaml

def parse_config(conf_path: pathlib.Path) -> dict:
    """Parses a config file to generate a dict.

    Should only be used on the files that contain a command.
    Not to be used on the main conf file.

    Args:
        conf_path (pathlib.Path): The path to the user's
        configuration file.

    Returns:
        dict: A dict that contains info on the command. The
        keys will either be `commands` or `expect`. Values
        should be `lists` of shell commands or stuff to
        expect before running those shell commands.
    """
    with open(conf_path, "r") as stream:
        conf = stream.read()

    parsed = yaml.safe_load(conf)

    return parsed

def check_config(conf: dict) -> None:
    """Checks the parsed configuration file for wrong types and arguments.

    This helps reduce weird error messages later on. It is easier for the
    user to interpret curated error messages than Python's default ones.
    This is especially true for `Pexpect`'s error messages. Timeouts can
    take a long time and the messages are often hard to read.

    Args:
        conf (dict): The parsed configuration file. This should be returned
            by `parse_config()`

    Raises:
        KeyError: If the configuration file has too many keys (more than 2).
        KeyError: If a key is named differently than `commands` or `expect`.
    """

    if not isinstance(conf, dict):
        raise TypeError(f"The configuration file must be seen as a dictionary. Currently seen as {type(conf)}")

    if len(conf.keys()) > 2:
        raise KeyError(
            f"Your configuration file must only have 2 keys, not {len(conf.keys())}"
        )
    for key, value in conf.items():
        if key not in ("commands", "expect"):
            raise KeyError(
                "Every key in your configuration file must be either 'commands' or 'expect'."
            )
        # value is of type `list`
        for item in value:

            if not isinstance(item, (str, dict)):

                print("Warning: keys should probably be of type `str` or `dict`.")
                print(
                    f"The parameter '{item}' from '{key}' has been interpreted as '{type(value)}'."
                )
                shoud_continue = input(
                    "Are you sure you still want to proceed (yes/no)? "
                )

                if shoud_continue.lower() not in ("yes", "no"):
                    while not shoud_continue.lower() in ("yes", "no"):
                        shoud_continue = input(
                            "Are you sure you still want to proceed (yes/no)? "
                        )

                if shoud_continue.lower() != "yes":
                    print("Quitting...")
                    sys.exit()

def check_parsed_config_no_interaction(conf_path: pathlib.Path) -> None:
    """
    check_parsed_config_no_interaction makes sure that a configuration file
    is valid. The configuration file is parsed using ``parse_config()```.

    Once the configuration file is unmarshalled, the result is checked for:

    - type is dict.
    - No more than two keys.
    - Keys are `commands` or `expect`.

    Parameters
    ----------
    conf_path: pathlib.Path
        The path towards the configuration file to check. Can be relative
        or absolute.
    """
    conf = parse_config(conf_path)

    if not isinstance(conf, dict):
        raise TypeError(f"The configuration file must be seen as a dictionary. Currently seen as {type(conf)}")

    if len(conf.keys()) > 2:
        raise KeyError(
            f"Your configuration file must only have 2 keys, not {len(conf.keys())}"
        )
    for key, value in conf.items():
        if key not in ("commands", "expect"):
            raise KeyError(
                "Every key in your configuration file must be either 'commands' or 'expect'."
            )

#######################################################################
#                             Debugging                               #
#######################################################################

if __name__ == "__main__":

    parse_config(pathlib.Path("./runner/tests/examples/test_conf.yaml"))
