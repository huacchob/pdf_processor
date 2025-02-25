"""Initialize the PDF Parser module."""

from .pdf import BaseBook, ChemBook, ITBook

__all__: list[str] = ["BaseBook", "ITBook", "ChemBook"]
