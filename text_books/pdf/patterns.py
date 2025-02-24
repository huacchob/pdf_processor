import re


class RegexPatterns:
    """Regex patterns used in the program."""

    @staticmethod
    def page_num_pipe_label() -> re.Pattern[str]:
        """
        Pattern to match a page number followed by a pipe and a label.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^(?P<num>\d+)\s\|\s(?P<label>.+)$")

    @staticmethod
    def label_pipe_page_num() -> re.Pattern[str]:
        """
        Pattern to match a label followed by a pipe and a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^(?P<label>.+?)\s\|\s(?P<num>\d+)$")

    @staticmethod
    def only_page_number() -> re.Pattern[str]:
        """
        Pattern to match a page number.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"^\s*(?P<page_num>\d+?)\s*$")

    @staticmethod
    def chapter_in_page() -> re.Pattern[str]:
        """
        Pattern to match a chapter in a page.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"(?i)\bchapter\b")

    @staticmethod
    def page_labels_to_ignore() -> re.Pattern[str]:
        """
        Pattern to match a page label to ignore.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"index|afterword", flags=re.IGNORECASE)

    @staticmethod
    def text_to_ignore() -> re.Pattern[str]:
        """
        Pattern to match a page label to ignore.

        Returns:
            re.Pattern[str]: Regex pattern.
        """
        return re.compile(pattern=r"oreilly\.com", flags=re.IGNORECASE)
