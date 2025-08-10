This project is a tool for extracting specific pages from a PDF document that belong to certain chapters. It supports handling different types of books, specifically IT books and Chemistry books, and allows the user to define a range of pages to extract.

### Features

- **Book Type Selection**: Users can choose between IT books and Chemistry books, each with predefined front and back matter pages to be excluded from the extraction.
- **Page Range Specification**: Users can specify a range of pages to extract using the `--pages` flag in the format of a tuple, e.g., `(1,10)`.
- **PDF Handling**: Utilizes the PyPDF2 library to read from and write to PDF files. It ensures that the output PDF does not overwrite existing files by deleting them if they exist.
- **Chapter Page Extraction**: Automatically determines and extracts pages that are considered part of the main chapters of the book, excluding front and back matter pages.

### Usage

1. Navigate to the top-level `text_books` directory.
2. Run the script using the command provided in the example above.
3. Specify the desired book type and page range as needed.

### Dependencies

- Python 3.12
- PyPDF2

### Notes

- Ensure that the input PDF path is correct; otherwise, a `FileNotFoundError` will be raised.
- The output PDF will be saved at the specified path, and a message will be printed confirming its creation.

To run this script, go to the top-level, same level as **text_books** directory.
Run the command `python3 -m text_books.main "path/to/original/pdf" "path/to/new/pdf" --book_type="Chem" --pages="(0,10)"`. The count starts from 0

The **book_type** flag should be set to either "Chem" or "IT".
The **pages** flag should be set to a tuple of two integers, e.g. "(0,10)".
