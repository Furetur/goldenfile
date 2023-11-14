from pathlib import Path
from typing import Optional, Sequence
from goldenfile.comparison import cmp_file, diff_file

from goldenfile.model import ExecutedTest


def print_diffs(executed_tests: Sequence[ExecutedTest]) -> None:
    def print_diff(test: ExecutedTest) -> None:
        checks = [
            ("stdout", test.test.golden_stdout, test.output.actual_stdout),
            ("stderr", test.test.golden_stderr, test.output.actual_stderr),
            # TODO
            # ("generated file", test.test.golden_generated_file, test.output.actual_generated_file),
        ]
        print(f" === {test.test.name}")
        for name, golden, actual in checks:
            if golden is None:
                continue
            if not cmp_file(golden, actual):
                print(f" ----- {name} Diff -----")
                print(diff_file(golden, actual))

    for t in executed_tests:
        print_diff(t)
