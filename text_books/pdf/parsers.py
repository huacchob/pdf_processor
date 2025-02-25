"""Module to extract pages from a PDF that belong to chapters."""

from array import array
from typing import Protocol, Sequence, runtime_checkable

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2._page import PageObject

from .handler import HandleBook


@runtime_checkable
class Book(Protocol):
    """Base Protocol."""

    def __init__(
        self,
        input_pdf: str,
        output_pdf: str,
        page_range: Sequence[int] | None = None,
    ) -> None:
        """Initialize the ParsePDF class."""
        ...

    def pdf_handler(self) -> None:
        """Initialize the HandleBook class."""
        ...

    def all_chapter_pages(self) -> None:
        """Determine if a page is a chapter page."""
        ...

    def within_page_range(self) -> None:
        """Add pages to the writer."""
        ...

    def run(self) -> None:
        """Run the main method to parse a PDF and extract chapter pages."""
        ...


class ITBook:
    """Parse a PDF and extract chapter pages."""

    PRELIMINARY_PAGES: int = 29
    BACK_MATTER_PAGES: int = 24

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

    def pdf_handler(self) -> None:
        """Initialize the HandleBook class."""
        self.book_handler: HandleBook = HandleBook(
            input_pdf=self.input_pdf,
        )
        self.book_handler.delete_file_if_exists(output_pdf=self.output_pdf)
        self.reader: PdfReader = self.book_handler.create_reader()
        self.writer: PdfWriter = self.book_handler.create_writer()

    def all_chapter_pages(self) -> None:
        """Determine if a page is a chapter page."""
        chapter_pages: list[PageObject] = self.reader.pages[
            self.PRELIMINARY_PAGES : -self.BACK_MATTER_PAGES
        ]
        for page in chapter_pages:
            self.writer.add_page(page=page)

    def within_page_range(self) -> None:
        """Add pages to the writer."""
        if not self.page_range:
            return
        start, end = self.page_range
        page_numbers: array[int] = array(
            "i",
            range(
                start + self.PRELIMINARY_PAGES,
                end + self.PRELIMINARY_PAGES + 1,
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
            self.all_chapter_pages()
        if self.page_range:
            self.within_page_range()

        if len(self.writer.pages) != 0:
            print(
                f"New PDF saved as '{self.output_pdf}'.",
            )


class ChemBook:
    """Parse a PDF and extract chapter pages."""

    PRELIMINARY_PAGES: int = 36
    BACK_MATTER_PAGES: int = 58

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

    def pdf_handler(self) -> None:
        """Initialize the HandleBook class."""
        self.book_handler: HandleBook = HandleBook(
            input_pdf=self.input_pdf,
        )
        self.book_handler.delete_file_if_exists(output_pdf=self.output_pdf)
        self.reader: PdfReader = self.book_handler.create_reader()
        self.writer: PdfWriter = self.book_handler.create_writer()

    def all_chapter_pages(self) -> None:
        """Determine if a page is a chapter page."""
        chapter_pages: list[PageObject] = self.reader.pages[
            self.PRELIMINARY_PAGES : -self.BACK_MATTER_PAGES
        ]
        for page in chapter_pages:
            self.writer.add_page(page=page)

    def within_page_range(self) -> None:
        """Add pages to the writer."""
        if not self.page_range:
            return
        start, end = self.page_range
        page_numbers: array[int] = array(
            "i",
            range(
                start + self.PRELIMINARY_PAGES,
                end + self.PRELIMINARY_PAGES + 1,
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
            self.all_chapter_pages()
        if self.page_range:
            self.within_page_range()

        if len(self.writer.pages) != 0:
            print(
                f"New PDF saved as '{self.output_pdf}'.",
            )
