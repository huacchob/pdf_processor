import re
from typing import Protocol


class RegexPatterns(Protocol):
    """Regex patterns used in the program."""

    @staticmethod
    def page_num_and_label() -> re.Pattern[str]:
        """
        Pattern to match a page number followed by a label.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        ...

    @staticmethod
    def label_and_page_num() -> re.Pattern[str]:
        """
        Pattern to match a label followed by a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        ...

    @staticmethod
    def only_page_number_pages() -> re.Pattern[str]:
        """
        Pattern to match when a page only has a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        ...

    @staticmethod
    def text_if_only_page_num() -> re.Pattern[str]:
        """
        Text to look for when a page only has a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        ...


class ITBookPatterns:
    """Regex patterns used in the program."""

    @staticmethod
    def page_num_and_label() -> re.Pattern[str]:
        """
        Pattern to match a page number followed by a pipe and a label.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^(?P<num>\d+)\s\|\s(?P<label>.+)$")

    @staticmethod
    def label_and_page_num() -> re.Pattern[str]:
        """
        Pattern to match a label followed by a pipe and a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^(?P<label>.+?)\s\|\s(?P<num>\d+)$")

    @staticmethod
    def only_page_number_pages() -> re.Pattern[str]:
        """
        Pattern to match when a page only has a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^\s*(?P<page_num>\d+?)\s*$")

    @staticmethod
    def text_if_only_page_num() -> re.Pattern[str]:
        """
        Text to look for when a page only has a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"(?i)\bchapter\b")

    @staticmethod
    def page_labels_to_ignore() -> re.Pattern[str]:
        """
        Page label patterns to ignore.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"index|afterword", flags=re.IGNORECASE)

    @staticmethod
    def text_to_ignore() -> re.Pattern[str]:
        """
        Page text patterns to ignore.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"oreilly\.com", flags=re.IGNORECASE)


class ChemBookPatterns:
    """Regex patterns used in the program."""

    @staticmethod
    def page_num_and_label() -> re.Pattern[str]:
        """
        Pattern to match a page number followed by a pipe and a label.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(
            pattern=r"^\s*(?P<num>\d+)\s*(?P<label>Chapter.+?)\s*$",
        )

    @staticmethod
    def label_and_page_num() -> re.Pattern[str]:
        """
        Pattern to match a label followed by a pipe and a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(
            pattern=r"^(?P<label>SECTION\s+[\d\.]+.+?)\s+(?P<num>\d+)$",
        )

    @staticmethod
    def only_page_number_pages() -> re.Pattern[str]:
        """
        Pattern to match when a page only has a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^\s*(?P<page_num>\d+?)\s*$")

    @staticmethod
    def text_if_only_page_num() -> re.Pattern[str]:
        """
        Text to look for when a page only has a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(
            pattern=r"^\s*Before\s+You\s+Begin,\s+Review\s+These\s+Skills\s*$",
        )

    @staticmethod
    def text_if_no_page_num() -> re.Pattern[str]:
        """
        Text to look for if the page is a chapter page, without a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(
            pattern=r"^\s*Chapter\s*$",
        )
