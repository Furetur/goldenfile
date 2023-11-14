from pathlib import Path
from typing import Optional, Sequence
from goldenfile.comparison import cmp_file, diff_file

from goldenfile.model import ExecutedTest, TestSuiteExecutionResult


def print_diffs(result: TestSuiteExecutionResult) -> None:
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

    for t in result.failed:
        print_diff(t)
    print(
        f"Summary: PASSED {len(result.passed)} FAILED {len(result.failed)} SKIPPED {len(result.skipped)}"
    )
