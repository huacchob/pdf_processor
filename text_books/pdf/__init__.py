"""Initialize the pdf module."""

from .book import BaseBook, ChemBook, ITBook

__all__: list[str] = ["ITBook", "ChemBook", "BaseBook"]
