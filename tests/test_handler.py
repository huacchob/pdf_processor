from pathlib import Path

from PyPDF2 import PdfWriter
from PyPDF2.errors import EmptyFileError

from text_books.pdf.handler import HandleBook


class TestHandler:
    """Test HandleBook class."""

    def test_handle_book_delete_file_if_exists(self) -> None:
        """Test method that deletes the output file if the file exists."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "test.pdf"
        output_file.touch()
        assert output_file.exists()
        handler = HandleBook(input_pdf=str(output_file))
        handler.delete_file_if_exists(output_pdf=str(output_file))
        assert not output_file.exists()

    def test_handle_book_delete_file_if_not_exists(self) -> None:
        """Test method that deletes the output file if the file does not exist."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "test.pdf"
        assert not output_file.exists()
        handler = HandleBook(input_pdf=str(output_file))
        handler.delete_file_if_exists(output_pdf=str(output_file))
        assert not output_file.exists()

    def test_create_reader_successful(self) -> None:
        """Test method that creates a PDF reader object."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "fixtures/sample_pdf.pdf"
        handler = HandleBook(input_pdf=str(output_file))
        handler.create_reader()

    def test_create_reader_empty_file_error(self) -> None:
        """Test method that creates a PDF reader object with an empty file."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "test.pdf"
        output_file.touch()
        handler = HandleBook(input_pdf=str(output_file))
        try:
            handler.create_reader()
        except EmptyFileError:
            assert True
        output_file.unlink()

    def test_create_reader_file_not_found(self) -> None:
        """Test method that creates a PDF reader object with a non-existent file."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "test.pdf"
        handler = HandleBook(input_pdf=str(output_file))
        try:
            handler.create_reader()
        except FileNotFoundError:
            assert True

    def test_create_writer(self) -> None:
        """Test method that creates a PDF writer object."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "test.pdf"
        handler = HandleBook(input_pdf=str(output_file))
        handler.create_writer()

    def test_add_pages_to_writer_successful(self) -> None:
        """Test method that creates add pages to a PDF writer object pass."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "fixtures/sample_pdf.pdf"
        handler = HandleBook(input_pdf=str(output_file))
        writer: PdfWriter = handler.create_writer()
        handler.add_pages_to_writer(
            page_nums=[i for i in range(10)],
            writer=writer,
            reader=handler.create_reader(),
        )

    def test_add_pages_to_writer_fail(self) -> None:
        """Test method that creates add pages to a PDF writer object fail."""
        cur_dir: Path = Path(__file__)
        output_file: Path = cur_dir.parent / "fixtures/sample_pdf.pdf"
        handler = HandleBook(input_pdf=str(output_file))
        writer: PdfWriter = handler.create_writer()
        try:
            handler.add_pages_to_writer(
                page_nums=[i for i in range(20)],
                writer=writer,
                reader=handler.create_reader(),
            )
        except IndexError:
            assert True
