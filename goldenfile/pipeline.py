from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from goldenfile.model import (
    Checker,
    Reporter,
    Runner,
    TagFilter,
    Test,
    TestDiscoverer,
    TestSuiteExecutionResult,
)


def has_no_golden_files(test: Test) -> bool:
    return (
            test.golden_generated_file is None
            and test.golden_stderr is None
            and test.golden_stdout is None
    )


@dataclass(frozen=True)
class Pipeline:
    test_discoverer: TestDiscoverer
    runner: Runner
    checker: Checker
    reporters: Sequence[Reporter]
    tag_filter: TagFilter = lambda _: True

    def run(self, test_suite_dir: Path) -> None:
        tests = self.test_discoverer(test_suite_dir)
        filtered_tests = [t for t in tests if self.tag_filter(t.tags)]
        executed_tests = set(self.runner(filtered_tests))
        skipped_tests = set(t for t in executed_tests if has_no_golden_files(t.test))
        passed_tests = set(
            t for t in (executed_tests - skipped_tests) if self.checker(t)
        )
        failed_tests = executed_tests - skipped_tests - passed_tests
        result = TestSuiteExecutionResult(
            passed=sorted(passed_tests, key=lambda t: t.test.name),
            failed=sorted(failed_tests, key=lambda t: t.test.name),
            skipped=sorted(skipped_tests, key=lambda t: t.test.name)
        )
        for reporter in self.reporters:
            reporter(result)
