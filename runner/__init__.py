# -*- coding: utf-8 -*-
""" Good-bot's command runner.

This module provides a command runner for Good-bot. It is used
to simulate a human typing commands to the shell. ``good-bot-runner``
uses ``pexpect`` to expect answers and respond accordingly.

Example:
    This programs reads a ``yaml`` file containing instrucitons on
    what to run and what to expect. Some examples on the syntax are
    provided in the ``tests`` directory. From this program's root
    directory::

        $ pip install .
        $ runner tests/examples/test_conf.yaml
    
"""

__version__ = "1.0.0"
