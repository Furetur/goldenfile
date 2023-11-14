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


def cmp_dir(lhs: Path, rhs: Path, shallow: bool = True) -> bool:
    if not lhs.is_dir():
        raise GoldenfileError(f"Incorrect directory: {lhs}")

    if not rhs.is_dir():
        raise GoldenfileError(f"Incorrect directory: {rhs}")

    # NOTE: Recursively traversing all subfoldres of a target directories
    #       and compare them.
    if not shallow:
        return _cmp_dir(lhs, rhs)

    difference: dircmp = dircmp(lhs, rhs)
    return difference.left_only or difference.right_only or difference.diff_files


def diff_dir(lhs: Path, rhs: Path, shallow: bool = True) -> bool:
    raise NotImplementedError()
