"""comparison -- module that provides ability to compare strings, files and directories."""


from typing import Callable, Any, Iterator
from difflib import context_diff, unified_diff
from filecmp import cmp
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


def cmp_dir(lhs: Path, rhs: Path, shallow: bool = True) -> bool:
    raise NotImplementedError()


def diff_dir(lhs: Path, rhs: Path, shallow: bool = True) -> bool:
    raise NotImplementedError()
