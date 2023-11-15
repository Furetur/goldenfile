from pathlib import Path
from typing import Sequence
from goldenfile.checker import bytewise_checker
from goldenfile.reporters.html_reporter import HtmlDiffReporter
from goldenfile.reporters.unify_diff import UnifyDiffReporter
from goldenfile.reporters.save_report import save_report
from goldenfile.reporters.replace_golden import ReplaceGoldenReporter
from goldenfile.runner import ShellCommand, shell_runner
from goldenfile.test_discoverers.simple_discoverer import simple_discoverer
from goldenfile.pipeline import Pipeline
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--replace", dest="replace", action="store_true", default=False)
(options, args) = parser.parse_args()
assert len(args) == 0

should_replace = [ReplaceGoldenReporter] if options.replace else []


class Python3ShellCommand(ShellCommand):
    def make_command(self, *, input_path: Path, output: Path) -> Sequence[str]:
        return ["python3", str(input_path)]


pipeline = Pipeline(
    test_discoverer=simple_discoverer,
    runner=shell_runner(Python3ShellCommand()),
    checker=bytewise_checker,
    reporters=[UnifyDiffReporter, HtmlDiffReporter, save_report(Path("temp/report.json"))] + should_replace
)

if __name__ == '__main__':
    pipeline.run(Path("example"))
