import os.path
import pathlib

from goldenfile.comparison import cmp_file, diff_file

from goldenfile.model import ExecutedTest, TestSuiteExecutionResult
from goldenfile.reporters.base_reporter import BaseReporter
from termcolor import cprint, colored


class UnifyDiffReporter(BaseReporter):

    @staticmethod
    def show_diff(result: TestSuiteExecutionResult) -> None:
        def print_failed_tests_diff(test: ExecutedTest) -> None:
            checks = [
                ("stdout", test.test.golden_stdout, test.output.actual_stdout),
                ("stderr", test.test.golden_stderr, test.output.actual_stderr),
                # TODO
                # ("generated file", test.test.golden_generated_file, test.output.actual_generated_file),
            ]

            for name, golden, actual in checks:
                if golden is None:
                    continue
                if not cmp_file(golden, actual):
                    cprint(f"Test \"{test.test.name}\" failed. ", color='red', end='')
                    diff = diff_file(golden, actual)
                    diff_path = pathlib.Path(actual).parent / f"{test.test.name}.diff"
                    print(diff, file=open(str(diff_path), "w"))
                    print(f"See diff at {diff_path}")

        for t in result.failed:
            print_failed_tests_diff(t)

        for t in result.passed:
            cprint(f"Test \"{t.test.name}\" passed.", color='green')

        for t in result.skipped:
            cprint(f"Test \"{t.test.name}\" skipped.", color='yellow')

        passed_str = colored(f"PASSED {len(result.passed)}", color='green')
        failed_str = colored(f"FAILED {len(result.failed)}", color='red')
        skipped_str = colored(f"SKIPPED {len(result.skipped)}", color='yellow')
        cprint(
            f"\nSummary: {passed_str} {failed_str} {skipped_str}",
        )
