import os.path
import pathlib

from goldenfile.comparison import cmp_file, diff_file

from goldenfile.model import ExecutedTest, TestSuiteExecutionResult
from goldenfile.reporters.base_reporter import BaseReporter
from termcolor import cprint, colored


class SummaryReporter(BaseReporter):
    @staticmethod
    def show_diff(result: TestSuiteExecutionResult) -> None:
        cprint("---------------", attrs=["bold"])
        cprint("Summary:\n", attrs=["bold"])
        SummaryReporter.print_passed_tests_colored(result)
        SummaryReporter.print_skipped_tests_colored(result)
        SummaryReporter.print_failed_tests_colored(result)
        SummaryReporter.print_summary_colored(result)


unify_diff_reporter = SummaryReporter.show_diff
