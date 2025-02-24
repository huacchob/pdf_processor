import re

from .exceptions import ImproperPageRange


def parse_tuple(range_str: str) -> tuple[int, int]:
    """
    Parse a string representing a tuple of two integers, e.g. '(1,10)'.

    Args:
        range_str (str): The input string.

    Returns:
        Tuple[int, int]: A tuple of two integers.

    Raises:
        argparse.ArgumentTypeError: If the input is not in the correct format.
    """
    match_start_end: re.Pattern[str] = re.compile(
        pattern=r"^(\(|\[)\s*(?P<start>\d+?)\s*,\s*(?P<end>\d+?)\s*(\)|\])$",
    )
    if start_end := match_start_end.search(string=range_str.strip()):
        try:
            start: int = int(start_end.group("start"))
            end: int = int(start_end.group("end"))
        except ValueError:
            raise ImproperPageRange(
                "Both values in the tuple must be integers",
            )
    else:
        raise ImproperPageRange("Must be a tuple of two integers, e.g. (1,10)")

    return (start, end)
