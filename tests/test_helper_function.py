from text_books.helper_funcs import parse_tuple


class TestHelperFunctions:
    def test_parse_tuple_tuple_with_comma(self) -> None:
        """Test that parse_tuple returns a tuple of two integers."""
        assert parse_tuple(range_str="(1,10)") == (1, 10)

    def test_parse_tuple_tuple_with_hyphen(self) -> None:
        """Test that parse_tuple returns a tuple of two integers."""
        assert parse_tuple(range_str="(1-10)") == (1, 10)

    def test_parse_tuple_list_with_comma(self) -> None:
        """Test that parse_tuple returns a tuple of two integers."""
        assert parse_tuple(range_str="[1,10]") == (1, 10)

    def test_parse_tuple_list_with_hyphen(self) -> None:
        """Test that parse_tuple returns a tuple of two integers."""
        assert parse_tuple(range_str="[1-10]") == (1, 10)

    def test_parse_tuple_string_comma(self) -> None:
        """Test that parse_tuple returns a tuple of two integers."""
        assert parse_tuple(range_str="1,10") == (1, 10)

    def test_parse_tuple_string_hyphen(self) -> None:
        """Test that parse_tuple returns a tuple of two integers."""
        assert parse_tuple(range_str="1-10") == (1, 10)
