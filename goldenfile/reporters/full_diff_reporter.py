from pathlib import Path
import subprocess
from typing import Optional

from termcolor import cprint
from goldenfile.comparison import cmp_whatever
from goldenfile.model import TestSuiteExecutionResult


def full_diff_reporter(result: TestSuiteExecutionResult) -> None:
    def print_diff(name: str, golden: Optional[Path], actual: Path) -> None:
        if golden is None:
            return
        if cmp_whatever(golden, actual):
            return
        cprint(name.upper(), attrs=["bold"])
        result = subprocess.Popen(
            ["diff", "--color=always", "-r", str(golden), str(actual)],
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        if result.stdout is None:
            return
        for line in result.stdout:
            if not line.startswith("diff"):
                print(line, end="")

    for test in result.failed:
        cprint(f"\n--- FAILED: {test.test.name}\n", color="red", attrs=["bold"])
        print_diff("stdout", test.test.golden_stdout, test.output.actual_stdout)
        print_diff("stderr", test.test.golden_stderr, test.output.actual_stderr)
        print_diff(
            "generated files",
            test.test.golden_generated_file,
            test.output.actual_generated_file,
        )
