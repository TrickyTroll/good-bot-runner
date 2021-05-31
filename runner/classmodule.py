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
        self.initial = commands[0]
        # The other commands will be sent using send.
        self.commands = commands[1:]
        self.expect = expect
        self.dir_name = "commands"

    def fake_start(self, text: str) -> None:
        """To print the first command before creating a child process.

        Args:
            text (str): The command that will be used to spawn a child
            process with pexpect.

        Returns:
            None: None
        """

        letters = list(text)
        for letter in letters[0:-1]:
            print(letter, end="", flush=True)
            time.sleep(0.11)  # TODO: This should be randomized.
        print(letters[-1])

        return None

    def get_directory(self) -> str:
        """Returns the dir_name attr.

        Returns:
            str: The dir_name.
        """
        return self.dir_name

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

        child.logfile = None
        child.logfile_read = sys.stdout
        child.delaybeforesend = 1
        child.sendline(secret)
        child.logfile = sys.stdout
        child.logfile_read = None

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

        return password

    def run(self) -> None:
        """Runs the command and anwsers all prompts for the sequence.

        Returns:
            None: None
        """
        child = pexpect.spawn("bash", echo=False)
        child.logfile = sys.stdout.buffer
        # TODO: This should be changed for a better regex
        # (check for the EOL).
        child.expect("[#$%]")

        self.fake_typing(child, self.initial)
        for i in range(len(self.commands)):
            if self.is_password(self.commands[i]):
                password = self.get_secret(self.commands[i])
                self.fake_typing(child, password)
            else:
                if self.expect[i] == "prompt":
                    child.expect("[#$%]")
                else:
                    child.expect(self.expect[i])

                self.fake_typing(child, self.commands[i])

        child.expect("[#$%]")
        child.close()

        return None
