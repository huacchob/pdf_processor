"""Module to extract pages from a PDF that belong to chapters."""

import argparse

from . import BaseBook, ChemBook, ITBook
from .helper_funcs import parse_tuple

book_class_mapper: dict[str, type[BaseBook]] = {
    "IT": ITBook,
    "Chem": ChemBook,
}


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
    parser.add_argument(
        "--book_type",
        choices=list(book_class_mapper),
        help="Select the book type to parse.",
    )
    args: argparse.Namespace = parser.parse_args()

    book_class_mapper[args.book_type](
        input_pdf=args.input_pdf,
        output_pdf=args.output_pdf,
        page_range=args.pages if args.pages else None,
    ).run()


if __name__ == "__main__":
    main()
