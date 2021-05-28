# -*- coding: utf-8 -*-
"""Functions to help with fake typing on the command line."""
import random

def is_typo() -> bool:
    """
    Determines wether or not a combination of key presses should 
    generate a typo. For now, we assume that every key press has
    an equal chance of being a typo.

    According to some papers[0], there is between 0.62% and 3.2%
    chances that a keypress will be a typo. For our purposes, we
    will assume that this percentage is between 1 and 3 percent.

    [0]: Refer the documentation.

    Returns:
        bool: Whether or not there will be a typo.

    """
    error_percent = random.randrange(1,4)/100 # Stop isn't included.
    # Randint includes the upper bound.
    return random.randint(0, 100) < error_percent
    