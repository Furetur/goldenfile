import abc

from termcolor import cprint, colored

from goldenfile import TestSuiteExecutionResult


class BaseReporter(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def show_diff(result: TestSuiteExecutionResult) -> None:
        pass

    @staticmethod
    def print_failed_tests_colored(result: TestSuiteExecutionResult):
        for t in result.failed:
            cprint(f"Test \"{t.test.name}\" failed.", color='red')

    @staticmethod
    def print_passed_tests_colored(result: TestSuiteExecutionResult):
        for t in result.passed:
            cprint(f"Test \"{t.test.name}\" passed.", color='green')

    @staticmethod
    def print_skipped_tests_colored(result: TestSuiteExecutionResult):
        for t in result.skipped:
            cprint(f"Test \"{t.test.name}\" skipped.", color='yellow')

    @staticmethod
    def print_summary_colored(result: TestSuiteExecutionResult):
        passed_str = colored(f"PASSED {len(result.passed)}", color='green')
        failed_str = colored(f"FAILED {len(result.failed)}", color='red')
        skipped_str = colored(f"SKIPPED {len(result.skipped)}", color='yellow')

        cprint(
            f"\nTotal: {passed_str} {failed_str} {skipped_str}",
        )

