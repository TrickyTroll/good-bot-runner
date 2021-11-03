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


@click.command()
@click.argument("input", type=str)
@click.option("--docker", default=False, help="Override the automatic environment selection.")
@click.option("--no-docker", default=False, help="Override the automatic environment selection.")
def gb_run(input: str, docker: bool, no_docker: bool) -> None:
    """Runs a command using the Commands class.
    It runs the command according to the configuration file that is
    passed as the 'input' argument
    """
    global DATA_DIR

    if in_docker():
        DATA_DIR = pathlib.Path("/data")
    else:
        DATA_DIR = pathlib.Path(".")

    # Overriding the automatic selection if the flags are not set to default.
    if docker:
        DATA_DIR = pathlib.Path("/project")
    elif no_docker:
        DATA_DIR = pathlib.Path(".")

    config_file_path: pathlib.Path = DATA_DIR / pathlib.Path(input)
    try:
        parsed = funcmodule.parse_config(config_file_path)
    except FileNotFoundError:
        funcmodule.config_not_found_routine(config_file_path, DATA_DIR)
    # parse_config does not assume anything about the config file.
    funcmodule.check_config(parsed)

    try:
        commands = parsed["commands"]
        expect = parsed["expect"]

    except KeyError:
        print("Missing element in the dictionary.")
        sys.exit()

    command = classmodule.Commands(commands, expect)

    command.run()

    return None


@click.command()
@click.argument("input-file", type=str)
def check_config(input_file: str) -> None:
    """Checks you configuration file to make sure that there are no errors."""
    try:
        funcmodule.check_parsed_config_no_interaction(DATA_DIR / pathlib.Path(input_file))
    except FileNotFoundError:
        funcmodule.config_not_found_routine(DATA_DIR / pathlib.Path(input_file), DATA_DIR)


def main():
    gb_run()
