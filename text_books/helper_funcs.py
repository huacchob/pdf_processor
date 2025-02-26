"""Argparse helper functions."""

import re

from .exceptions import ImproperPageRange


def parse_tuple(range_str: str) -> tuple[int, int]:
    """
    The function `parse_tuple` takes a string representing a range and returns
    a tuple of two integers representing the start and end of the range.

    Args:
      range_str (str): The `range_str` parameter is a string that represents a
        range in the format of a tuple. The tuple should contain two integers
        separated by a comma or a hyphen, enclosed in either square brackets
        `[ ]`parentheses `( )`, or neither. For example, valid input for
        `range_str`could be "(1,10)", "(1-10)", "[1-10]",, "[1,10]", "1-10", or
        "1,10", while invalid input could be "(1,10,20)", or "[1-10-20]".

    Returns:
      The function `parse_tuple` is returning a tuple containing two integers
      extracted from the input `range_str`. The integers represent the start
      and end values parsed from the input string.
    """
    match_start_end: re.Pattern[str] = re.compile(
        pattern=r"^(\(|\[)*\s*(?P<start>\d+?)\s*(,|-)\s*(?P<end>\d+?)\s*(\)|\])*$",
    )
    if start_end := match_start_end.search(string=range_str.strip()):
        try:
            start: int = int(start_end.group("start"))
            end: int = int(start_end.group("end"))
        except ValueError as e:
            raise ImproperPageRange(
                "Both values in the tuple must be integers",
            ) from e
    else:
        raise ImproperPageRange("Must be a tuple of two integers, e.g. (1,10)")

    return (start, end)
