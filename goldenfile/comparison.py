"""comparison -- module that provides ability to compare strings, files and directories."""


from typing import Callable, Any


def _default_str_comparator(lhs: str, rhs: str) -> bool:
    return lhs == rhs


def cmp_str(
    lhs: str,
    rhs: str,
    *,
    comparator: Callable[[str, str], Any] = _default_str_comparator
) -> Any:
    return comparator(lhs, rhs)
