# -*- coding: utf-8 -*-
"""``good-bot-runner``'s main module.

This module contains the code for the program's command
line interface. ``runner`` uses the
`click <https://click.palletsprojects.com/en/7.x/>`
library for its /CLI/.

See click's
`documentation <https://click.palletsprojects.com/en/7.x/#documentation>`
for more information on how decorators affect the ``gb_run()`` function.
"""

import os
import sys
import click
import pathlib
from runner import classmodule
from runner import funcmodule


def in_docker() -> bool:
    """Checks if code is currently running in a Docker container.
    Checks if Docker is in control groups or if there is a `.dockerenv`
    file at the filesystem's root directory.
    Returns:
        bool: Whether or not the code is running in a Docker container.
    """
    path = "/proc/self/cgroup"
    return (
        os.path.exists("/.dockerenv")
        or os.path.isfile(path)
        and any("docker" in line for line in open(path))
    )


if in_docker():
    DATA_DIR = pathlib.Path("/data")
else:
    DATA_DIR = pathlib.Path(".")


@click.command()
@click.argument("input", type=str)
def gb_run(input: str) -> None:
    """Runs a command using the Commands class.
    It runs the command according to the configuration file that is
    passed as the 'input' argument
    """
    parsed = funcmodule.parse_config(DATA_DIR / pathlib.Path(input))

    try:
        commands = parsed["commands"]
        expect = parsed["expect"]

    except KeyError:
        print("Missing element in the dictionary.")
        sys.exit()

    command = classmodule.Commands(commands, expect)

    command.run()

    return None


def main():
    gb_run()
