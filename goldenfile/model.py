from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Sequence

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


@dataclass(frozen=True)
class TestOutput:
    actual_stdout: Path
    actual_stderr: Path
    actual_generated_file: Path


@dataclass(frozen=True)
class ExecutedTest:
    test: Test
    output: TestOutput

TestDiscoverer = Callable[[Path], Sequence[Test]]

Runner = Callable[[Sequence[Test]], Sequence[ExecutedTest]]

Reporter = Callable[[Sequence[ExecutedTest]], None]
