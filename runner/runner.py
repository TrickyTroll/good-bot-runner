# -*- coding: utf-8 -*-
"""`good-bot-runner`'s main module.

This module contains the code for the program's command
line interface. `runner` uses the
[click](https://click.palletsprojects.com/en/7.x/)
library for its *CLI*.

See click's
[documentation](https://click.palletsprojects.com/en/7.x/#documentation)
for more information on how decorators affect the `gb_run()` function.
"""

import sys
import click
from runner import classmodule
from runner import funcmodule


@click.command()
@click.argument("input", type=click.File("r"))
def gb_run(input: click.File) -> None:
    """Runs a command using the Commands class.
    It runs the command according to the configuration file that is
    passed as the 'input' argument
    """
    parsed = funcmodule.parse_config(input)

    try:
        commands = parsed["commands"]
        expect = parsed["expect"]

    except KeyError:
        print("Missing element in the dictionary.")
        sys.exit()

    command = classmodule.Commands(commands, expect)

    command.run()

    return None


# if __name__ == "__main__":
#     gb_run()
def main():
    gb_run()
