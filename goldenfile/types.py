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

    
