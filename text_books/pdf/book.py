"""Module to extract pages from a PDF that belong to chapters."""

from array import array
from pathlib import Path
from typing import Sequence

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2._page import PageObject

from .handler import HandleBook


class BaseBook:
    """Base Book Class."""

    FRONT_MATTER_PAGES: int = 0
    BACK_MATTER_PAGES: int = 0

    def __init__(
        self,
        input_pdf: str,
        output_pdf: str,
        page_range: Sequence[int] | None = None,
    ) -> None:
        """Initialize the BaseBook class."""
        """
        Initializes the BaseBook class with input and output PDF paths,
        optional page range, and object attributes.
        
        Args:
          input_pdf (str): The `input_pdf` parameter is a string that
            represents the file path of the input PDF file that will be
            processed by the BaseBook class.
          output_pdf (str): A string that represents the path or filename of
            the output PDF file where the processed PDF will be saved.
          page_range (Sequence[int] | None): Used to specify a sequence of page
            numbers from the input PDF that should be processed. If
            `page_range` is set to `None`, it means that all pages in the input
            PDF will be processed.
        """
        # Arguments
        self.input_pdf: str = input_pdf
        self.output_pdf: str = output_pdf
        self.page_range: Sequence[int] | None = page_range

        # Objects
        self.book_handler: HandleBook
        self.reader: PdfReader
        self.writer: PdfWriter

    def pdf_handler(self) -> None:
        """
        Initializes the HandleBook class, deletes the output PDF file if it
        exists, and creates PdfReader and PdfWriter objects.
        """
        self.book_handler: HandleBook = HandleBook(
            input_pdf=self.input_pdf,
        )
        self.book_handler.delete_file_if_exists(output_pdf=self.output_pdf)
        self.reader: PdfReader = self.book_handler.create_reader()
        self.writer: PdfWriter = self.book_handler.create_writer()

    def all_chapter_pages(self) -> None:
        """
        This function determines if a page is a chapter page and adds it to the
        writer.
        """
        chapter_pages: list[PageObject] = self.reader.pages[
            self.FRONT_MATTER_PAGES : -self.BACK_MATTER_PAGES
        ]
        for page in chapter_pages:
            self.writer.add_page(page=page)

    def within_page_range(self) -> None:
        """
        This function adds pages to the writer within a specified page range.

        Returns:
          If the `self.page_range` is empty, the function will return None.
          Otherwise, it will add pages to the writer based on the specified
          page range.
        """
        """Add pages to the writer."""
        if not self.page_range:
            return
        start, end = self.page_range
        page_numbers: array[int] = array(
            "i",
            range(
                start + self.FRONT_MATTER_PAGES,
                end + self.FRONT_MATTER_PAGES + 1,
            ),
        )
        self.book_handler.add_pages_to_writer(
            page_nums=page_numbers,
            writer=self.writer,
            reader=self.reader,
        )

    def run(self) -> None:
        """
        The `run` method parses a PDF, extracts chapter pages, and saves the
        output as a new PDF file.
        """
        self.pdf_handler()
        if not self.page_range:
            self.all_chapter_pages()
        if self.page_range:
            self.within_page_range()

        self.book_handler.write_to_file(
            output_pdf=self.output_pdf,
            writer=self.writer,
        )

        if Path(self.output_pdf).exists():
            print(
                f"New PDF saved as '{self.output_pdf}'.",
            )


class ITBook(BaseBook):
    """Parse a PDF and extract chapter pages for IT."""

    FRONT_MATTER_PAGES: int = 20
    BACK_MATTER_PAGES: int = 24


class ChemBook(BaseBook):
    """Parse a PDF and extract chapter pages for Chemistry."""

    FRONT_MATTER_PAGES: int = 36
    BACK_MATTER_PAGES: int = 58
