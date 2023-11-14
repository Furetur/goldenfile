from pathlib import Path
from typing import Callable, Sequence, Optional
from dataclasses import dataclass

Tag = str
TagFilter = Callable[[Sequence[Tag]], bool]

@dataclass(frozen=True)
class Test:
    name: str
    tags: Sequence[Tag]
    input: Path
    golden_stdout: Optional[Path]
    golden_stderr: Optional[Path]
    golden_generated_file: Optional[Path]


INPUT_SUFFIX = ".input"
STDOUT_SUFFIX = ".stdout"
STDERR_SUFFIX = ".stderr"
GENERATED_FILE_SUFFIX = ".gen"

def load_tags(test_dir: Path) -> Sequence[Tag]:
    config_files = [p for p in test_dir.iterdir() if p.is_file() and p.suffixes]

def discover(test_suite_dir: Path, tag_filter: TagFilter) -> Sequence[Test]:
    test_dirs = [p for p in test_suite_dir.iterdir() if p.is_dir()]
    for test_dir in test_dirs:
