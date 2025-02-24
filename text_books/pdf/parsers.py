"""Module to extract pages from a PDF that belong to chapters."""

import re
from array import array
from typing import Protocol, Sequence, runtime_checkable

from PyPDF2 import PdfReader, PdfWriter

from .handler import HandleBook
from .patterns import ITBookPatterns as it

PRELIMINARY_PAGES: int = 29  # starts at 0


@runtime_checkable
class Book(Protocol):
    """Base Protocol."""

    def pdf_handler(self) -> None:
        """Initialize the HandleBook class."""
        ...

    def is_chapter_page(self, text: str) -> bool:
        """
        Determine if a page is a chapter page.

        Args:
            text (str): The text of the page

        Returns:
            bool: True if the page is a chapter page
        """
        ...

    def within_page_range(self) -> None:
        """Add pages to the writer."""
        ...

    def run(self) -> None:
        """Run the main method to parse a PDF and extract chapter pages."""
        ...


class ITBook:
    """Parse a PDF and extract chapter pages."""

    def __init__(
        self,
        input_pdf: str,
        output_pdf: str,
        page_range: Sequence[int] | None = None,
    ) -> None:
        """Initialize the ParsePDF class."""
        # Arguments
        self.input_pdf: str = input_pdf
        self.output_pdf: str = output_pdf
        self.page_range: Sequence[int] | None = page_range

        # Objects
        self.book_handler: HandleBook
        self.reader: PdfReader
        self.writer: PdfWriter

        # Regex patterns
        self.pattern_num_pipe_label: re.Pattern[str] = it.page_num_and_label()
        self.pattern_label_pipe_num: re.Pattern[str] = it.label_and_page_num()
        self.chapter_in_page: re.Pattern[str] = it.text_if_only_page_num()
        self.only_page_number: re.Pattern[str] = it.only_page_number_pages()
        self.ignore_labels: re.Pattern[str] = it.page_labels_to_ignore()
        self.ignore_text: re.Pattern[str] = it.text_to_ignore()

    def pdf_handler(self) -> None:
        """Initialize the HandleBook class."""
        self.book_handler: HandleBook = HandleBook(
            input_pdf=self.input_pdf,
        )
        self.reader: PdfReader = self.book_handler.create_reader()
        self.writer: PdfWriter = self.book_handler.create_writer()

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
        for text_line in lines:
            if not text_line:
                continue
            line: str = text_line.strip()

            match1: re.Match[str] | None = self.pattern_num_pipe_label.match(
                string=line,
            )
            match2: re.Match[str] | None = self.pattern_label_pipe_num.match(
                string=line,
            )
            match3: re.Match[str] | None = self.only_page_number.match(
                string=line,
            )

            if match1:
                label_string: str = match1.group("label")
                if self.ignore_labels.search(
                    string=label_string.lower()
                ) or self.ignore_text.search(string=text):
                    continue
                is_valid: bool = True
                break

            elif match2:
                label_string: str = match2.group("label")
                if self.ignore_labels.search(
                    string=label_string.lower()
                ) or self.ignore_text.search(string=text):
                    continue
                is_valid: bool = True
                break

            elif match3:
                if self.chapter_in_page.search(string=text):
                    if self.ignore_text.search(string=text):
                        continue
                    is_valid: bool = True
                    break

        return is_valid

    def within_page_range(self) -> None:
        """Add pages to the writer."""
        if not self.page_range:
            return
        start, end = self.page_range
        page_numbers: array[int] = array(
            "i",
            range(
                start + PRELIMINARY_PAGES,
                end + PRELIMINARY_PAGES + 1,
            ),
        )
        self.book_handler.add_pages_to_writer(
            page_nums=page_numbers,
            writer=self.writer,
            reader=self.reader,
        )

    def run(self) -> None:
        """Run the main method to parse a PDF and extract chapter pages."""
        self.pdf_handler()
        if not self.page_range:
            for page in self.reader.pages:
                text: str = page.extract_text() or ""
                if self.is_chapter_page(text=text):
                    self.writer.add_page(page=page)
        if self.page_range:
            self.within_page_range()

        self.book_handler.write_to_file(
            output_pdf=self.output_pdf,
            writer=self.writer,
        )

        if len(self.writer.pages) != 0:
            print(
                f"New PDF saved as '{self.output_pdf}'.",
            )
