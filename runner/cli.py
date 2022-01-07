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

import click
import pathlib
import sys
from runner import commands_runner
from runner import funcmodule

DATA_DIR: pathlib.Path = pathlib.Path(".")

@click.command()
@click.argument("input_file", type=str)
@click.option(
    "--docker",
    type=bool,
    default=False,
    is_flag=True,
    help="Override the automatic environment selection.",
)
@click.option(
    "--no-docker",
    type=bool,
    default=False,
    is_flag=True,
    help="Override the automatic environment selection.",
)
def gb_run(input_file: str, docker: bool, no_docker: bool) -> None:
    """Runs a command using the Commands class.
    It runs the command according to the configuration file that is
    passed as the 'input' argument
    """

    if funcmodule.in_docker():
        DATA_DIR = pathlib.Path("/data")
    else:
        DATA_DIR = pathlib.Path(".")

    # Overriding the automatic selection if the flags are not set to default.
    if docker:
        DATA_DIR = pathlib.Path("/project")
    elif no_docker:
        DATA_DIR = pathlib.Path(".")

    config_file_path: pathlib.Path = DATA_DIR / pathlib.Path(input_file)
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

    command = commands_runner.Commands(commands, expect)

    command.run()

    print()


@click.command()
@click.argument("input-file", type=str)
def check_config(input_file: str) -> None:
    """Checks you configuration file to make sure that there are no errors."""
    try:
        funcmodule.check_parsed_config_no_interaction(
            DATA_DIR / pathlib.Path(input_file)
        )
    except FileNotFoundError:
        funcmodule.config_not_found_routine(
            DATA_DIR / pathlib.Path(input_file), DATA_DIR
        )


def main():
    gb_run()
