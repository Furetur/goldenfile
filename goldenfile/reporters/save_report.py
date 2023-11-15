from pathlib import Path, PurePath
from typing import Optional, Sequence, Callable
import json

from goldenfile.model import ExecutedTest, TestSuiteExecutionResult
from goldenfile.reporters.base_reporter import BaseReporter

def save_report(to: Path) -> Callable[[TestSuiteExecutionResult], None]:
    class SaveReporter(BaseReporter):
        @staticmethod
        def show_diff(result: TestSuiteExecutionResult) -> None:
            res = []
            def add_as(category: str, seq: Sequence[ExecutedTest]) -> None:
                for t in seq:
                    res.append({"name": t.test.name, "tags": t.test.tags, "result": category})
                pass
            add_as('passed', result.passed)
            add_as('failed', result.failed)
            add_as('skipped', result.skipped)
            with open(to, "w") as fle:
                fle.write(json.dumps(res))
    return SaveReporter
