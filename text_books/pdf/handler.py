from typing import Sequence

from PyPDF2 import PdfReader, PdfWriter


class HandleBook:
    def __init__(self, input_pdf: str) -> None:
        self.input_pdf: str = input_pdf
        self.reader: PdfReader

    def create_reader(self) -> PdfReader:
        """
        Create a PDF reader object from the input PDF file.

        Raises:
            FileNotFoundError: If the input PDF file is not found.

        Returns:
            PdfReader: A PDF reader object.
        """
        try:
            self.reader: PdfReader = PdfReader(stream=self.input_pdf)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File {self.input_pdf} not found.") from e
        return self.reader

    def create_writer(self) -> PdfWriter:
        """
        Create a PDF writer object.

        Returns:
            PdfWriter: A PDF writer object.
        """
        return PdfWriter()

    def write_to_file(self, output_pdf: str, writer: PdfWriter) -> None:
        with open(file=output_pdf, mode="wb") as f:
            writer.write(stream=f)  # type: ignore

    def add_pages_to_writer(
        self,
        page_nums: Sequence[int],
        writer: PdfWriter,
        reader: PdfReader,
    ) -> None:
        for page in page_nums:
            writer.add_page(page=reader.pages[page])
