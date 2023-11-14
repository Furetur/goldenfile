from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from goldenfile.model import Reporter, Runner, TagFilter, TestDiscoverer


@dataclass(frozen=True)
class Pipeline:
    test_discoverer: TestDiscoverer
    runner: Runner
    reporters: Sequence[Reporter]
    tag_filter: TagFilter = lambda _: True

    def run(self, test_suite_dir: Path) -> None:
        tests = self.test_discoverer(test_suite_dir)
        filtered_tests = [t for t in tests if self.tag_filter(t.tags)]
        executed_tests = self.runner(filtered_tests)
        for reporter in self.reporters:
            reporter(executed_tests)
