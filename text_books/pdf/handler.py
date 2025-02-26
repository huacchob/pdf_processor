"""Class for handling PDF files."""

from pathlib import Path
from typing import Sequence

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import EmptyFileError


class HandleBook:
    """Handles PDF files."""

    def __init__(self, input_pdf: str) -> None:
        """
        Initialize the HandleBook class.

        Args:
            input_pdf (str): The path to the input PDF file.
        """
        self.input_pdf: str = input_pdf
        self.reader: PdfReader

    def delete_file_if_exists(self, output_pdf: str) -> None:
        """
        Delete the input PDF file if it exists.

        Args:
            output_pdf (str): The path to the output PDF file.
        """
        Path(output_pdf).unlink(missing_ok=True)

    def create_reader(self) -> PdfReader:
        """
        Create a PDF reader object.

        Raises:
            FileNotFoundError: Raised when the input PDF file is not found.
            EmptyFileError: Raised when the input PDF file is an empty file.

        Returns:
            PdfReader: A PDF reader object.
        """
        try:
            self.reader: PdfReader = PdfReader(stream=self.input_pdf)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File {self.input_pdf} not found.") from e
        except EmptyFileError as e:
            raise EmptyFileError(f"File {self.input_pdf} is an empty file.") from e
        return self.reader

    def create_writer(self) -> PdfWriter:
        """
        Create a PDF writer object.

        Returns:
            PdfWriter: A PDF writer object.
        """
        return PdfWriter()

    def write_to_file(self, output_pdf: str, writer: PdfWriter) -> None:
        """
        Write the PDF writer object to a file.

        Args:
            output_pdf (str): The path to the output PDF file.
            writer (PdfWriter): The PDF writer object.
        """
        with open(file=output_pdf, mode="wb") as f:
            writer.write(stream=f)

    def add_pages_to_writer(
        self,
        page_nums: Sequence[int],
        writer: PdfWriter,
        reader: PdfReader,
    ) -> None:
        """
        Add pages to a PDF writer object.

        Args:
            page_nums (Sequence[int]): A sequence of page numbers.
            writer (PdfWriter): A PDF writer object.
            reader (PdfReader): A PDF reader object.

        Raises:
            IndexError: If a page number is out of range.
        """
        try:
            for page in page_nums:
                writer.add_page(page=reader.pages[page])
        except IndexError as e:
            raise IndexError(f"Page number {page} is out of range.") from e
