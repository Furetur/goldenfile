from pathlib import Path
from typing import Optional
from goldenfile.comparison import cmp_whatever
from goldenfile.model import ExecutedTest


def bytewise_checker(test: ExecutedTest) -> bool:
    def maybe_check(golden: Optional[Path], actual: Path) -> bool:
        if golden is None:
            return True
        else:
            return cmp_whatever(golden, actual)

    checks = [
        (test.test.golden_stdout, test.output.actual_stdout),
        (test.test.golden_stderr, test.output.actual_stderr),
        (test.test.golden_generated_file, test.output.actual_generated_file),
    ]
    return all(maybe_check(golden, actual) for golden, actual in checks)
