from textwrap import dedent
from pathlib import Path
from contextlib import contextmanager

from pytest import fixture, raises

from goldenfile.comparison import cmp_file
from goldenfile.exception import GoldenfileError


@fixture
def setup_success_identical(tmp_path):
    @contextmanager
    def context_manager():
        first = Path(tmp_path, "first")
        first.write_text(
            dedent(
                """\
                first
                second
                third
                """
            ),
            encoding="utf-8",
        )

        second = Path(tmp_path, "second")
        second.write_text(
            dedent(
                """\
                first
                second
                third
                """
            ),
            encoding="utf-8",
        )

        yield first, second

    return context_manager


def test_success_identical(
    setup_success_identical,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_identical() as (first, second):
        assert cmp_file(first, second)


@fixture
def setup_success_different(tmp_path):
    @contextmanager
    def context_manager():
        first = Path(tmp_path, "first")
        first.write_text(
            dedent(
                """\
                first
                second
                third
                different
                """
            ),
            encoding="utf-8",
        )

        second = Path(tmp_path, "second")
        second.write_text(
            dedent(
                """\
                first
                third
                second
                """
            ),
            encoding="utf-8",
        )

        yield first, second

    return context_manager


def test_success_different(
    setup_success_different,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_different() as (first, second):
        assert not cmp_file(first, second)


@fixture
def setup_incorrect_first_file(tmp_path):
    @contextmanager
    def context_manager():
        # NOTE: Didn't create a file just define some path.
        first = Path(tmp_path, "first")

        second = Path(tmp_path, "second")
        second.write_text(
            dedent(
                """\
                first
                third
                second
                """
            ),
            encoding="utf-8",
        )

        yield first, second

    return context_manager


def test_incorrect_first_file(
    setup_incorrect_first_file,  # pylint: disable=redefined-outer-name
    tmp_path,
) -> None:
    with raises(GoldenfileError) as exception:
        with setup_incorrect_first_file() as (first, second):
            cmp_file(first, second)

    expect: str = f"Incorrect file: {tmp_path}/first"
    actual: str = exception.value.message
    assert actual == expect


@fixture
def setup_second_file_is_directory(tmp_path):
    @contextmanager
    def context_manager():
        first = Path(tmp_path, "first")
        first.write_text(
            dedent(
                """\
                first
                third
                second
                """
            ),
            encoding="utf-8",
        )

        second = Path(tmp_path, "second")
        second.mkdir()

        yield first, second

    return context_manager


def test_second_file_is_directory(
    setup_second_file_is_directory,  # pylint: disable=redefined-outer-name
    tmp_path,
) -> None:
    with raises(GoldenfileError) as exception:
        with setup_second_file_is_directory() as (first, second):
            cmp_file(first, second)

    expect: str = f"Incorrect file: {tmp_path}/second"
    actual: str = exception.value.message
    assert actual == expect
