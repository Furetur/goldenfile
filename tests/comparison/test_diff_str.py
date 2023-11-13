from textwrap import dedent

from goldenfile.comparison import diff_str


def test_simple_string() -> None:
    first: str = "Hello"
    second: str = "heiio"

    expect: str = dedent(
        """\
        *** expect

        --- actual

        ***************

        *** 1,5 ****

        ! H
          e
        ! l
        ! l
          o
        --- 1,5 ----

        ! h
          e
        ! i
        ! i
          o"""
    )
    actual: str = diff_str(first, second)
    assert actual == expect


def test_multiline_string() -> None:
    first: str = dedent(
        """\
        first
        second
        third
        """
    )
    second: str = dedent(
        """\
        third
        second
        first
        """
    )

    expect: str = dedent(
        """\
        *** expect

        --- actual

        ***************

        *** 1,3 ****

          first
        - second
        - third
        --- 1,3 ----

        + third
        + second
          first"""
    )
    actual: str = diff_str(first, second)
    assert actual == expect


def test_one_string_multiline_string() -> None:
    first: str = "third"
    second: str = dedent(
        """\
        third
        second
        first
        """
    )

    expect: str = dedent(
        """\
        *** expect

        --- actual

        ***************

        *** 1 ****

        --- 1,3 ----

          third
        + second
        + first"""
    )
    actual: str = diff_str(first, second)
    assert actual == expect
