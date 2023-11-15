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
                    cprint(f'Test "{test.test.name}" failed. ', color="red", end="")
                    diff = diff_file(golden, actual)
                    diff_path = pathlib.Path(actual).parent / f"{test.test.name}.diff"
                    print(diff, file=open(str(diff_path), "w"))
                    print(f"See diff at {diff_path}")

        UnifyDiffReporter.print_passed_tests_colored(result)
        UnifyDiffReporter.print_skipped_tests_colored(result)
        UnifyDiffReporter.print_failed_tests_colored(result)
        UnifyDiffReporter.print_summary_colored(result)


unify_diff_reporter = UnifyDiffReporter.show_diff
