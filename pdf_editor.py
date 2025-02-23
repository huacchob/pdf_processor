import argparse
import re
import typing as t
from array import array

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2._page import PageObject

PRELIMINARY_PAGES: int = 29  # starts at 0


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
    def __init__(
        self,
        output_pdf: str,
        reader: PdfReader,
        writer: PdfWriter,
        page_range: tuple[int, int] | None = None,
    ) -> None:
        # Attributes
        self.output_pdf: str = output_pdf
        self.reader: PdfReader = reader
        self.writer: PdfWriter = writer
        self.page_range: tuple[int, int] | None = page_range

        self.valid_page_indices: list[t.Optional[int]] = []

        # Regex patterns
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

    def is_chapter_page(self, text: str) -> bool:
        """
        Determine if a page is a chapter page.

        Args:
            text (str): The text of the page

        Returns:
            bool: True if the page is a chapter page
        """
        is_valid: bool = False
        if not text:
            return is_valid

        label_string: str = ""
        lines: list[str] = text.splitlines()
        for line in lines:
            if not line:
                continue
            line: str = line.strip()

            match1 = self.pattern_num_pipe_label.match(string=line)
            match2 = self.pattern_label_pipe_num.match(string=line)
            match3 = self.simple_number_pattern.match(string=line)

            if match1:
                label_string = match1.group("label")
                if self.ignore_lables.search(
                    string=label_string.lower()
                ) or self.ignore_text.search(string=text):
                    continue
                is_valid = True
                break

            elif match2:
                label_string = match2.group("label")
                if self.ignore_lables.search(
                    string=label_string.lower()
                ) or self.ignore_text.search(string=text):
                    continue
                is_valid = True
                break

            elif match3:
                if self.chapter_in_page.search(string=text):
                    if self.ignore_text.search(string=text):
                        continue
                    is_valid = True
                    break

        return is_valid

    def within_page_range(self) -> None:
        """
        Determine if a page is within the page range.

        Returns:
            bool: True if the page is within the page range.
        """
        start, end = self.page_range
        page_numbers: array[int] = array(
            "i",
            range(
                start + PRELIMINARY_PAGES,
                end + PRELIMINARY_PAGES + 1,
            ),
        )
        for page in page_numbers:
            self.valid_page_indices.append(page)
            self.writer.add_page(page=self.reader.pages[page])

    def run(self) -> None:
        all_pages: t.List[PageObject] = self.reader.pages
        if not self.page_range:
            for i, page in enumerate(iterable=all_pages):
                text: str = page.extract_text() or ""
                if self.is_chapter_page(text=text):
                    self.valid_page_indices.append(i)
                    self.writer.add_page(page=page)
        if self.page_range:
            self.within_page_range()

        if not self.valid_page_indices:
            print("No valid chapter pages found.")
            return

        with open(file=self.output_pdf, mode="wb") as f:
            self.writer.write(stream=f)  # type: ignore

        print(f"New PDF with selected chapter pages saved as '{self.output_pdf}'.")


def extract_chapter_pages(
    input_pdf: str,
) -> tuple[PdfReader, PdfWriter]:
    """
    Extract pages from a PDF that belong to chapters (or their sub-sections).

    Args:
        input_pdf (str): Input PDF file path.
    """
    try:
        reader: PdfReader = PdfReader(stream=input_pdf)
    except FileNotFoundError as file:
        raise FileNotFoundError(f"File {input_pdf} not found.") from file
    return reader, PdfWriter()


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

    reader, writer = extract_chapter_pages(
        input_pdf=args.input_pdf,
    )

    pdf: ParsePDF = ParsePDF(
        output_pdf=args.output_pdf,
        reader=reader,
        writer=writer,
        page_range=args.pages if args.pages else None,
    )
    pdf.run()


if __name__ == "__main__":
    main()
