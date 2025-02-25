"""Initialize the pdf module."""

from .parsers import Book, ChemBook, ITBook

__all__: list[str] = ["ITBook", "ChemBook", "Book"]
