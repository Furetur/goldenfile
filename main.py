
from pathlib import Path
from typing import Sequence
from goldenfile.reporters.print_diffs import print_diffs
from goldenfile.runner import ShellCommand, shell_runner
from goldenfile.test_discoverers.simple_discoverer import simple_discoverer
from goldenfile.pipeline import Pipeline

class Python3ShellCommand(ShellCommand):
    def make_command(self, *, input: Path, output: Path) -> Sequence[str]:
        return ["python3", str(input)]

pipeline = Pipeline(
    test_discoverer=simple_discoverer,
    runner=shell_runner(Python3ShellCommand()),
    reporters=[print_diffs]
)

pipeline.run(Path("example"))
