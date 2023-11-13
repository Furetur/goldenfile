from textwrap import dedent

from goldenfile.comparison import cmp_str


def test_simple() -> None:
    assert cmp_str("aa12bb34cc56", "aa12bb34cc56")
    assert not cmp_str("aa123", "aa1234")


def test_custom_comparator() -> None:
    def custom_cmp(lhs: str, rhs: str) -> int:
        if len(lhs) > len(rhs):
            return 1

        if len(lhs) < len(rhs):
            return -1

        return 0

    assert cmp_str("aa12", "aa1", comparator=custom_cmp) == 1
    assert cmp_str("aa1", "aa12", comparator=custom_cmp) == -1
    assert cmp_str("abc", "cba", comparator=custom_cmp) == 0


def test_simple_compare_multiline_strings() -> None:
    lhs: str = dedent(
        """\
        Wow !
        It's
        so
        long
        multiline
        string
        """
    )

    rhs: str = dedent(
        """\
        Wow !
        It's
        so
        long
        multiline
        string
        """
    )

    assert cmp_str(lhs, rhs)


def test_advanced_compare_multiline_strings() -> None:
    def lines_cmp(lhs: str, rhs: str) -> bool:
        return len(lhs.splitlines()) >= len(rhs.splitlines())

    lhs: str = dedent(
        """\
        Wow !
        It's
        so
        long
        multiline
        string
        """
    )

    rhs: str = dedent(
        """\
        string
        multiline
        long
        so
        It's
        Wow !
        """
    )

    assert cmp_str(lhs, rhs, comparator=lines_cmp)
