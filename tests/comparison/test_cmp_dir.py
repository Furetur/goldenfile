from textwrap import dedent
from pathlib import Path
from contextlib import contextmanager

from pytest import fixture, raises

from goldenfile.comparison import cmp_dir
from goldenfile.exception import GoldenfileError


@fixture
def setup_success_identical(tmp_path):
    @contextmanager
    def context_manager():
        # First folder structure:
        # first/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        first = Path(tmp_path, "first")
        first.mkdir()

        first_sample: Path = Path(first, "sample.py")
        first_sample.write_text(
            dedent(
                """\
                Sample
                """
            ),
            encoding="utf-8",
        )

        first_subfolder: Path = Path(first, "subfolder")
        first_subfolder.mkdir()

        Path(first_subfolder, "subfolder-sample").touch()

        # Second folder structure:
        # second/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        second = Path(tmp_path, "second")
        second.mkdir()

        second_sample: Path = Path(second, "sample.py")
        second_sample.write_text(
            dedent(
                """\
                Sample
                """
            ),
            encoding="utf-8",
        )

        second_subfolder: Path = Path(second, "subfolder")
        second_subfolder.mkdir()

        Path(second_subfolder, "subfolder-sample").touch()

        yield first, second

    return context_manager


def test_success_identical_shallow(
    setup_success_identical,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_identical() as (first, second):
        assert cmp_dir(first, second)


def test_success_identical_deep(
    setup_success_identical,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_identical() as (first, second):
        assert cmp_dir(first, second, shallow=False)


@fixture
def setup_success_file_difference(tmp_path):
    @contextmanager
    def context_manager():
        # First folder structure:
        # first/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        first = Path(tmp_path, "first")
        first.mkdir()

        first_sample: Path = Path(first, "sample.py")
        first_sample.write_text(
            dedent(
                """\
                First Sample
                """
            ),
            encoding="utf-8",
        )

        first_subfolder: Path = Path(first, "subfolder")
        first_subfolder.mkdir()

        Path(first_subfolder, "subfolder-sample").touch()

        # Second folder structure:
        # second/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        second = Path(tmp_path, "second")
        second.mkdir()

        second_sample: Path = Path(second, "sample.py")
        second_sample.write_text(
            dedent(
                """\
                Second Sample
                """
            ),
            encoding="utf-8",
        )

        second_subfolder: Path = Path(second, "subfolder")
        second_subfolder.mkdir()

        Path(second_subfolder, "subfolder-sample").touch()

        yield first, second

    return context_manager


def test_success_file_difference(
    setup_success_file_difference,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_file_difference() as (first, second):
        assert not cmp_dir(first, second)


@fixture
def setup_success_structure_difference(tmp_path):
    @contextmanager
    def context_manager():
        # First folder structure:
        # first/
        #   sample.py

        first = Path(tmp_path, "first")
        first.mkdir()

        first_sample: Path = Path(first, "sample.py")
        first_sample.write_text(
            dedent(
                """\
                Sample
                """
            ),
            encoding="utf-8",
        )

        # Second folder structure:
        # second/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        second = Path(tmp_path, "second")
        second.mkdir()

        second_sample: Path = Path(second, "sample.py")
        second_sample.write_text(
            dedent(
                """\
                Sample
                """
            ),
            encoding="utf-8",
        )

        second_subfolder: Path = Path(second, "subfolder")
        second_subfolder.mkdir()

        Path(second_subfolder, "subfolder-sample").touch()

        yield first, second

    return context_manager


def test_success_structure_difference(
    setup_success_structure_difference,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_structure_difference() as (first, second):
        assert not cmp_dir(first, second)


@fixture
def setup_success_difference_shallow_and_deep(tmp_path):
    @contextmanager
    def context_manager():
        # First folder structure:
        # first/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        first = Path(tmp_path, "first")
        first.mkdir()

        first_sample: Path = Path(first, "sample.py")
        first_sample.write_text(
            dedent(
                """\
                Sample
                """
            ),
            encoding="utf-8",
        )

        first_subfolder: Path = Path(first, "subfolder")
        first_subfolder.mkdir()

        first_subfolder_sample: Path = Path(first_subfolder, "subfolder-sample")
        first_subfolder_sample.write_text(
            dedent(
                """\
                First Subfolder Sample
                """
            ),
            encoding="utf-8",
        )

        # Second folder structure:
        # second/
        #   sample.py
        #   subfolder/
        #     subfolder-sample

        second = Path(tmp_path, "second")
        second.mkdir()

        second_sample: Path = Path(second, "sample.py")
        second_sample.write_text(
            dedent(
                """\
                Sample
                """
            ),
            encoding="utf-8",
        )

        second_subfolder: Path = Path(second, "subfolder")
        second_subfolder.mkdir()

        second_subfolder_sample: Path = Path(second_subfolder, "subfolder-sample")
        second_subfolder_sample.write_text(
            dedent(
                """\
                Second Subfolder Sample
                """
            ),
            encoding="utf-8",
        )

        yield first, second

    return context_manager


def test_success_difference_shallow_and_deep(
    setup_success_difference_shallow_and_deep,  # pylint: disable=redefined-outer-name
) -> None:
    with setup_success_difference_shallow_and_deep() as (first, second):
        # Returns `True` because only top-level directories are compared
        # and subdirectories are not analyzed.
        assert cmp_dir(first, second, shallow=True)

        # Returns `False` because nested subdirectories are compared
        # recursively.
        assert not cmp_dir(first, second, shallow=False)


@fixture
def setup_incorrect_first_directory(tmp_path):
    @contextmanager
    def context_manager():
        # NOTE: Didn't create a directory just define some path.
        first = Path(tmp_path, "first")

        second = Path(tmp_path, "second")
        second.mkdir()

        yield first, second

    return context_manager


def test_incorrect_first_directory(
    setup_incorrect_first_directory,  # pylint: disable=redefined-outer-name
    tmp_path,
) -> None:
    with raises(GoldenfileError) as exception:
        with setup_incorrect_first_directory() as (first, second):
            cmp_dir(first, second)

    expect: str = f"Incorrect directory: {tmp_path}/first"
    actual: str = exception.value.message
    assert actual == expect


@fixture
def setup_second_file_is_file(tmp_path):
    @contextmanager
    def context_manager():
        first = Path(tmp_path, "first")
        first.mkdir()

        second = Path(tmp_path, "second")
        second.write_text(
            dedent(
                """\
                Not a directory :(
                """
            ),
            encoding="utf-8",
        )

        yield first, second

    return context_manager


def test_second_file_is_file(
    setup_second_file_is_file,  # pylint: disable=redefined-outer-name
    tmp_path,
) -> None:
    with raises(GoldenfileError) as exception:
        with setup_second_file_is_file() as (first, second):
            cmp_dir(first, second)

    expect: str = f"Incorrect directory: {tmp_path}/second"
    actual: str = exception.value.message
    assert actual == expect
