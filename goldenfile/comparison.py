"""comparison -- module that provides ability to compare strings, files and directories."""


from typing import Callable, Any
from difflib import context_diff


def _default_str_comparator(lhs: str, rhs: str) -> bool:
    return lhs == rhs


def cmp_str(
    lhs: str,
    rhs: str,
    *,
    comparator: Callable[[str, str], Any] = _default_str_comparator
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
