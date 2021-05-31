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

import sys
import yaml
from io import TextIOWrapper


def parse_config(conf: TextIOWrapper) -> dict:
    """Parses a config file to generate a dict.

    Should only be used on the files that contain a command.
    Not to be used on the main conf file.

    Args:
        conf (TextIOWrapper): The opened text file. This should
        be created by the 
        [click](https://click.palletsprojects.com/en/7.x/)
        library.

    Returns:
        dict: A dict that contains info on the command. The
        keys will either be `commands` or `expect`. Values
        should be `lists` of shell commands or stuff to
        expect before running those shell commands.
    """
    parsed = yaml.safe_load(conf)

    if type(parsed) != dict:
        print("Wrong type of config file.")
        sys.exit()

    return parsed


#######################################################################
#                             Debugging                               #
#######################################################################

if __name__ == "__main__":
    import os

    current_dir = os.getcwd()
    with open("./runner/tests/examples/test_conf.yaml", "r") as stream:
        parse_config(stream)
