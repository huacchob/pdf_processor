import argparse
import re
import typing as t
from array import array

from PyPDF2 import PdfReader, PdfWriter

PRELIMINARY_PAGES: int = 34  # starts at 0


class ImproperPageRange(Exception):
    pass


def parse_tuple(range_str: str) -> t.Tuple[int, int]:
    """
    Parse a string representing a tuple of two integers, e.g. "(1,10)".

    Args:
        s (str): The input string.

    Returns:
        Tuple[int, int]: A tuple of two integers.

    Raises:
        argparse.ArgumentTypeError: If the input is not in the correct format.
    """
    match_start_end: re.Pattern[str] = re.compile(
        pattern=r"^\s*\(\s*(?P<start>\d+?)\s*,\s*(?P<end>\d+?)\s*\)\s*$"
    )
    if start_end := match_start_end.search(string=range_str):
        try:
            start = int(start_end.group("start"))
            end = int(start_end.group("end"))
        except ValueError:
            raise ImproperPageRange(
                "Both values in the tuple must be integers",
            )
    else:
        raise ImproperPageRange("Must be a tuple of two integers, e.g. (1,10)")

    return (start, end)


class RegexPatternsMixin:
    @staticmethod
    def page_num_pipe_label() -> re.Pattern[str]:
        """
        Pattern to match a page number followed by a pipe and a label.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^(?P<num>\d+)\s\|\s(?P<label>.+)$")

    @staticmethod
    def label_pipe_page_num() -> re.Pattern[str]:
        """
        Pattern to match a label followed by a pipe and a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^(?P<label>.+?)\s\|\s(?P<num>\d+)$")

    @staticmethod
    def only_page_number() -> re.Pattern[str]:
        """
        Pattern to match a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^\s*(?P<page_num>\d+?)\s*$")

    @staticmethod
    def chapter_in_page() -> re.Pattern[str]:
        """
        Pattern to match a chapter in a page.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"(?i)\bchapter\b")

    @staticmethod
    def page_lables_to_ignore() -> re.Pattern[str]:
        """
        Pattern to match a page label to ignore.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"index|afterword", flags=re.IGNORECASE)

    @staticmethod
    def text_to_ignore() -> re.Pattern[str]:
        """
        Pattern to match a page label to ignore.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"oreilly\.com", flags=re.IGNORECASE)


class ParsePDF:
    def __init__(self, text: str) -> None:
        self.text: str = text
        self.is_valid: bool = False

        self.label_string: str = ""

        self.pattern_num_pipe_label: re.Pattern[str] = (
            RegexPatternsMixin.page_num_pipe_label()
        )
        self.pattern_label_pipe_num: re.Pattern[str] = (
            RegexPatternsMixin.label_pipe_page_num()
        )
        self.chapter_in_page: re.Pattern[str] = RegexPatternsMixin.chapter_in_page()
        self.simple_number_pattern: re.Pattern[str] = (
            RegexPatternsMixin.only_page_number()
        )
        self.ignore_lables: re.Pattern[str] = RegexPatternsMixin.page_lables_to_ignore()
        self.ignore_text: re.Pattern[str] = RegexPatternsMixin.text_to_ignore()

    def is_chapter_page(self) -> bool:
        """
        Determine if a page is a chapter page.

        Args:
            text (str): The text of the page

        Returns:
            bool: True if the page is a chapter page
        """
        lines: list[str] = self.text.splitlines()
        for line in lines:
            line: str = line.strip()
            if not line:
                continue

            match1: re.Match[str] | None = self.pattern_num_pipe_label.match(
                string=line,
            )
            if match1:
                self.label_string: str = match1.group("label")
                self.is_valid = True
                break

            match2: re.Match[str] | None = self.pattern_label_pipe_num.match(
                string=line,
            )
            if match2 and self.is_valid is False:
                self.label_string: str = match2.group("label")
                self.is_valid = True
                break

        # Check for a line that is just a page number.
        if self.is_valid is False:
            for line in lines:
                if not line:
                    continue
                line = line.strip()
                if self.simple_number_pattern.match(string=line):
                    if self.chapter_in_page.search(string=self.text):
                        self.is_valid = True
                        break

        if self.ignore_lables.search(
            string=self.label_string
        ) or self.ignore_text.search(
            string=self.text,
        ):
            self.is_valid = False

        return self.is_valid

    def is_within_page_range(self, page_range: tuple[int, int]) -> bool:
        """
        Determine if a page is within the page range.

        Args:
            text (str): The text of the page

        Returns:
            bool: True if the page is within the page range.
        """
        start, end = page_range
        page_numbers: array[int] = array("i", range(start, end + 1))
        for page in page_numbers:
            page_num: int = page_num + PRELIMINARY_PAGES
            try:
                
        


def extract_chapter_pages(
    input_pdf: str,
    output_pdf: str,
    page_range: t.Optional[tuple[int, int]] = None,
) -> None:
    """
    Extract pages from a PDF that belong to chapters (or their sub-sections).

    Args:
        input_pdf (str): Input PDF file path.
        output_pdf (str): Output PDF file path.
    """
    reader: PdfReader = PdfReader(stream=input_pdf)
    writer: PdfWriter = PdfWriter()
    valid_page_indices: list[t.Optional[int]] = []

    for i, page in enumerate(iterable=reader.pages):
        text: str = page.extract_text() or ""
        pdf_parser: ParsePDF = ParsePDF(text=text)
        if not page_range and pdf_parser.is_chapter_page():
            valid_page_indices.append(i)
            writer.add_page(page=page)
        elif page_range and pdf_parser.is_within_page_range(
            page_range=page_range,
        ):
            valid_page_indices.append(i)
            writer.add_page(page=page)
            if len(writer.pages) == (page_range[1] + 1) - page_range[0]:
                break

    if not valid_page_indices:
        print("No valid chapter pages found.")
        return

    with open(file=output_pdf, mode="wb") as f:
        writer.write(stream=f)  # type: ignore

    print(f"New PDF with selected chapter pages saved as '{output_pdf}'.")


def main() -> None:
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

    extract_chapter_pages(
        input_pdf=args.input_pdf,
        output_pdf=args.output_pdf,
        page_range=args.pages if args.pages else None,
    )


if __name__ == "__main__":
    main()
