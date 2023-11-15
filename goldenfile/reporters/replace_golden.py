from pathlib import Path, PurePath
from typing import Optional, Sequence
import shutil

from goldenfile.model import ExecutedTest, TestSuiteExecutionResult
from goldenfile.reporters.base_reporter import BaseReporter

class ReplaceGoldenReporter(BaseReporter):
    @staticmethod
    def show_diff(result: TestSuiteExecutionResult) -> None:
        def copy_file(golden: Optional[Path], actual: Path) -> None:
            if golden is not None:
                shutil.copy(golden, actual.with_suffix(actual.suffix + ".bck"))
            if actual.is_file() and golden is not None:
                shutil.copy(actual, golden)
        for t in result.failed:
            copy_file(t.test.golden_stdout, t.output.actual_stdout)
            copy_file(t.test.golden_stderr, t.output.actual_stderr)
            copy_file(t.test.golden_generated_file, t.output.actual_generated_file)
