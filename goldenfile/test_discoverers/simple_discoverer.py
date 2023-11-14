from pathlib import Path
from typing import Callable, Sequence, Optional
from dataclasses import dataclass
import yaml
from goldenfile.constants import CONFIG_SUFFIX, GENERATED_FILE_SUFFIX, INPUT_SUFFIX, STDERR_SUFFIX, STDOUT_SUFFIX

from goldenfile.model import Tag, Test


def read_test(test_dir: Path) -> Test:
    test_name = test_dir.stem

    def read_tags() -> Sequence[Tag]:
        with open(test_dir / (test_name + CONFIG_SUFFIX)) as file:
            return yaml.safe_load(file)["tags"]

    def get_file(suffix: str) -> Optional[Path]:
        matching_files = [p for p in test_dir.iterdir() if suffix in p.suffixes]
        if len(matching_files) == 0:
            return None
        else:
            return matching_files[0]

    return Test(
        name=test_name,
        tags=tuple(read_tags()),
        # TODO: this allows input to be none, however it is not possible
        input=get_file(INPUT_SUFFIX),
        golden_stdout=get_file(STDOUT_SUFFIX),
        golden_stderr=get_file(STDERR_SUFFIX),
        golden_generated_file=get_file(GENERATED_FILE_SUFFIX)
    )


def simple_discoverer(test_suite_dir: Path) -> Sequence[Test]:
    test_dirs = (p for p in test_suite_dir.iterdir() if p.is_dir())
    return [read_test(test_dir) for test_dir in test_dirs]
