"""Module to extract pages from a PDF that belong to chapters."""

import argparse

from . import ITBook
from .helper_funcs import parse_tuple


def main() -> None:
    """Run the main function."""
    parser = argparse.ArgumentParser(
        description="Extract pages from a PDF that belong to chapters.",
    )
    parser.add_argument("input_pdf", help="Path to the input PDF file.")
    parser.add_argument("output_pdf", help="Path for the output PDF file.")
    parser.add_argument(
        "--pages",
        type=parse_tuple,
        help="A tuple of two integers, e.g. '(1,10)'",
    )
    args: argparse.Namespace = parser.parse_args()

    ITBook(
        input_pdf=args.input_pdf,
        output_pdf=args.output_pdf,
        page_range=args.pages if args.pages else None,
    ).run()


if __name__ == "__main__":
    main()
