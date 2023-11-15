from pathlib import Path
from typing import Sequence
from goldenfile.checker import bytewise_checker
from goldenfile.reporters.html_reporter import HtmlDiffReporter
from goldenfile.reporters.unify_diff import UnifyDiffReporter
from goldenfile.runner import ShellCommand, shell_runner
from goldenfile.test_discoverers.simple_discoverer import simple_discoverer
from goldenfile.pipeline import Pipeline


class Python3ShellCommand(ShellCommand):
    def make_command(self, *, input_path: Path, output: Path) -> Sequence[str]:
        return ["python3", str(input_path)]


pipeline = Pipeline(
    test_discoverer=simple_discoverer,
    runner=shell_runner(Python3ShellCommand()),
    checker=bytewise_checker,
    reporters=[UnifyDiffReporter, HtmlDiffReporter]
)

if __name__ == '__main__':
    pipeline.run(Path("example"))
