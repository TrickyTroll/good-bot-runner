# -*- coding: utf-8 -*-
"""Functions to help with fake typing on the command line."""
import random

LEFT_HAND = ["as", "sa", "er", "re", "sd", "ds", "ec", "ce", "ew", "we", "wa", "aw", "cr", "sc", "cs"]
RIGHT_HAND = ["lk", "lo", "ol", "op", "po", "io", "oi", "no", "on", "in", "ni"]
HAND_ALTERNATION = ["al", "la", "ak", "ka", "am", "ma", "an", "na", "ai", "ia", "so", "os", "sp", "ps", "en", "ne", "em", "me", "el", "le", "ep", "pe"]

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

def get_delay(previous_letter: str, next_letter: str) -> float:
    """Function to get the delay before the next letter is typed.

    This function uses the fact that letters typed by two different
    hands will usually be typed 30 to 60ms faster than two letters
    pressed by the same hand.

    There is also an average delay of betweem 120 and 170ms between
    two keystrokes.

    Args:
        previous_letter (str): The previously typed letter.
        next_letter (str): The next letter to type.

    Returns:
        float: The time **in seconds** before the next keystroke.
            This value is calculated using the previous and next
            letter.
    """
    avg_delay = random.randint(120, 170)/1000 # in seconds
    if previous_letter+next_letter in HAND_ALTERNATION:
        # Two letters typed by different hands are 30-60ms faster.
        faster_by = random.randint(30, 60)/1000
        avg_delay -= faster_by
    return avg_delay
