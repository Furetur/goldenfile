import abc

from goldenfile import TestSuiteExecutionResult


class BaseReporter(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def show_diff(result: TestSuiteExecutionResult) -> None:
        pass
