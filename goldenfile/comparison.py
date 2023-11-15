"""comparison -- module that provides ability to compare strings, files and directories."""


from typing import Callable, Any, Iterator
from difflib import context_diff, unified_diff
from filecmp import cmp, dircmp
from pathlib import Path

from .exception import GoldenfileError


def _default_str_comparator(lhs: str, rhs: str) -> bool:
    return lhs == rhs


def cmp_str(
    lhs: str,
    rhs: str,
    *,
    comparator: Callable[[str, str], Any] = _default_str_comparator,
) -> Any:
    return comparator(lhs, rhs)


def diff_str(lhs: str, rhs: str) -> str:
    if len(lhs.splitlines()) > 1 or len(rhs.splitlines()) > 1:
        return "\n".join(
            context_diff(
                lhs.splitlines(),
                rhs.splitlines(),
                fromfile="expect",
                tofile="actual",
            )
        )

    return "\n".join(context_diff(lhs, rhs, fromfile="expect", tofile="actual"))


def cmp_file(lhs: Path, rhs: Path) -> bool:
    if not lhs.is_file():
        raise GoldenfileError(f"Incorrect file: {lhs}")

    if not rhs.is_file():
        raise GoldenfileError(f"Incorrect file: {rhs}")

    return cmp(lhs, rhs, shallow=False)


def diff_file(lhs: Path, rhs: Path) -> str:
    if not lhs.is_file():
        raise GoldenfileError(f"Incorrect file: {lhs}")

    if not rhs.is_file():
        raise GoldenfileError(f"Incorrect file: {rhs}")

    lhs_content: str = lhs.read_text(encoding="utf-8")
    rhs_content: str = rhs.read_text(encoding="utf-8")

    difference: Iterator[str] = unified_diff(
        lhs_content.splitlines(),
        rhs_content.splitlines(),
        lineterm="",
        fromfile=str(lhs),
        tofile=str(rhs),
    )

    return "\n".join(difference)


def _cmp_dir(lhs: Path, rhs: Path) -> bool:
    difference: dircmp = dircmp(lhs, rhs)

    if difference.left_only or difference.right_only or difference.diff_files:
        return False

    for subdir in difference.common_dirs:
        lhs_subdir: Path = Path(lhs, subdir)
        rhs_subdir: Path = Path(rhs, subdir)
        if not _cmp_dir(lhs_subdir, rhs_subdir):
            return False

    return True


def cmp_dir(lhs: Path, rhs: Path, *, shallow: bool = True) -> bool:
    if not lhs.is_dir():
        raise GoldenfileError(f"Incorrect directory: {lhs}")

    if not rhs.is_dir():
        raise GoldenfileError(f"Incorrect directory: {rhs}")

    # NOTE: Recursively traversing all subdirectories of a target directories
    #       and compare them.
    if not shallow:
        return _cmp_dir(lhs, rhs)

    difference: dircmp = dircmp(lhs, rhs)
    difference_len: int = len(
        difference.left_only or difference.right_only or difference.diff_files
    )
    return difference_len == 0


def _diff_dir(lhs: Path, rhs: Path) -> bool:
    difference: dircmp = dircmp(lhs, rhs)

    if difference.left_only or difference.right_only or difference.diff_files:
        return False

    for subdir in difference.common_dirs:
        lhs_subdir: Path = Path(lhs, subdir)
        rhs_subdir: Path = Path(rhs, subdir)
        if not _cmp_dir(lhs_subdir, rhs_subdir):
            return False

    return True


class DifferenceDirecoriesFilesStorage:
    def __init__(self):
        self.left_only: list[Path] = []
        self.right_only: list[Path] = []
        self.diff_files: list[Path] = []

    def append(self, lhs: Path, rhs: Path) -> None:
        difference: dircmp = dircmp(lhs, rhs)

        if difference.left_only:
            left_only = [Path(lhs, item) for item in difference.left_only]
            self.left_only.extend(left_only)

        if difference.right_only:
            right_only = [Path(rhs, item) for item in difference.right_only]
            self.right_only.extend(right_only)

        if difference.diff_files:
            files = [
                (Path(lhs, item), Path(rhs, item)) for item in difference.diff_files
            ]
            self.diff_files.extend(files)

    def __str__(self) -> str:
        output: str = ""

        for left_only_file in self.left_only:
            output += f"-{left_only_file}\n"

        for right_only_file in self.right_only:
            output += f"+{right_only_file}\n"

        output += "\n"

        for lhs_file, rhs_file in self.diff_files:
            output += f"{diff_file(lhs_file, rhs_file)}\n\n"

        # NOTE: Remove extra newline
        output = output.rsplit("\n", 1)[0]
        return output


def _diff_dir(
    lhs: Path,
    rhs: Path,
    diff_files: DifferenceDirecoriesFilesStorage = DifferenceDirecoriesFilesStorage(),
) -> None:
    diff_files.append(lhs, rhs)
    for subdir in dircmp(lhs, rhs).common_dirs:
        lhs_subdir: Path = Path(lhs, subdir)
        rhs_subdir: Path = Path(rhs, subdir)
        _diff_dir(lhs_subdir, rhs_subdir, diff_files)


def diff_dir(lhs: Path, rhs: Path, shallow: bool = True) -> str:
    if not lhs.is_dir():
        raise GoldenfileError(f"Incorrect directory: {lhs}")

    if not rhs.is_dir():
        raise GoldenfileError(f"Incorrect directory: {rhs}")

    diff_files = DifferenceDirecoriesFilesStorage()

    if cmp_dir(lhs, rhs, shallow=shallow):
        return diff_files

    if not shallow:
        _diff_dir(lhs, rhs, diff_files)
    else:
        diff_files.append(lhs, rhs)

    return str(diff_files)
