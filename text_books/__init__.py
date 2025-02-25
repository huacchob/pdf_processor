"""Initialize the PDF Parser module."""

from .pdf import Book, ChemBook, ITBook

__all__: list[str] = ["Book", "ITBook", "ChemBook"]
