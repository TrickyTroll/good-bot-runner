# -*- coding: utf-8 -*-
"""Classes used by the `runner` program.

This module contains the class used by `runner` create `Commands`
objects.

## Example:

To create a `Commands object`:

```python
import classmodule
todo = Commands(self, ["echo 'Hello, World!'"], ["prompt"])
```
    
`todo` will be an object of type `Commands`. The `run()`
method should be used to spawn a new shell process and start
*typing* the commands.:

```python
todo.run()
```
"""
import pexpect
import sys
import os
import time
from typing import Union, List, Dict

from runner import human_typing


class Commands:
    def __init__(self, commands: list, expect: list):
        # The first command will be typed using fake_typing.
        # The other commands will be sent using send.
        self.commands = commands
        self.expect = expect
        # `dir_name` should be set dynamically.
        self.dir_name = "commands"

    def fake_typing(self, child: pexpect.pty_spawn.spawn, text: str) -> None:
        """Fake typing of commands

        This function uses the `type_sentence()` function from the
        `human_typing` module.

        This function adds typos and delays to make the typing as
        human-like as possible.

        Args:
            text (str): The text to type
            child (pexpect.pty_spawn.spawn): The child process.

        """
        human_typing.type_sentence(child, text)

    def fake_typing_secret(self, child: pexpect.pty_spawn.spawn, secret: str) -> None:
        """To fake type a password or other secret. This ensures that the
        password won't be recorded.

        Args:
            secret (str): The secret that has to be typed
            child (pexpect.pty_spawn.spawn): The child process.

        """
        if not isinstance(secret, str):
            raise TypeError(f"Secret must be of type string, not {type(secret)}.")

        listed = list(secret)
        # Adding newline if missing.
        if listed[-1] != "\n":
            listed.append("\n")

        # Turning off echo and logging. We don't want the password to be shown.
        child.logfile = None
        for item in listed:
            child.send(item)
        # Getting things back to normal.
        child.logfile = sys.stdout

    def is_password(self, command: Union[str, dict]) -> bool:
        """
        Checks if the next thing that will be sent to the child
        process is a password.

        Args:
            command (Union[str, dict]): The next command to send
                to the child process.

        Returns:
            bool: Whether or not `command` is a password.
        """

        if isinstance(command, dict):
            if "password" in command.keys():
                return True

        return False

    def get_secret(self, command: dict) -> str:
        """Gets a password value from an environment variable.

        The variable should be defined by the user in the project's
        configuration file.

        Args:
            command (dict): A value in the configuration
                file's `commands` field. This value can only
                be of type `dict` since `get_secret()` should only
                be called after checking that the `command` is a
                password to send.

        Returns:
            str: A password to send to the child process.
        """
        env_key = [item for item in command.values()][0]
        password = os.getenv(env_key)

        if not password:

            raise ValueError(f"The environment variable {env_key} wasn't set.")

        return password

    def run(self) -> None:
        """Runs the command and anwsers all prompts for the sequence.

        This starts by spawning a `bash` process and expecting the
        bash prompt.

        After the prompt has been detected, the first item in the
        list of commands is sent to the child process using `Commands`'
        `fake_typing()` method.

        The program then expects the first iem in the `expect` list.
        These steps are repeated until every command has been sent and
        completed.

        `password` elements are replaced by their corresponding value
        in the environment variables.

        """
        child = pexpect.spawn("bash", echo=False, encoding="utf-8")
        child.logfile = sys.stdout
        child.expect("[#\$%]")

        for index, command in enumerate(self.commands):

            expect = self.expect[index]

            if self.is_password(command):

                password = self.get_secret(command)
                self.fake_typing_secret(child, password)

            else:

                self.fake_typing(child, command)

            if expect == "prompt":
                child.expect("[#\$%]")
            # wait for process to be over here
            elif expect == "EOP":
                pas
                # Wait until end of process
                # while !(process_over(command)):
                #     pass
                #     child.expect("[#\$%]")
            else:
                child.expect(expect)

        child.close()

        return None
