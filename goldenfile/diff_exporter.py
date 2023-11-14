import logging
import os
import goldenfile.comparison as comparison

from typing import List
from goldenfile import Result

__all__ = ["DiffExporter"]


class DiffExporter:
    def __init__(self, test_suite_name: str, expected: List[Result], actual: List[Result]):
        self.logger = logging.getLogger(test_suite_name)
        self.default_logging_level = logging.INFO
        self.c_logger = None
        self.f_logger = None
        if len(expected) != len(actual):
            raise AttributeError(f"Expected length ({len(expected)}) != actual length ({len(actual)})")
        self.expected = expected
        self.actual = actual

    def set_console_logger(self):
        self.c_logger = logging.StreamHandler()
        self.logger.addHandler(self.c_logger)
        return self

    def set_file_logger(self, destination_path: str | os.PathLike):
        self.f_logger = logging.FileHandler(filename=destination_path)
        self.logger.addHandler(self.f_logger)
        return self

    def log_diff(self):
        # TODO: Handle case with no loggers
        for expected_unit, actual_unit in zip(self.expected, self.actual):
            # TODO: diff_dir
            diff = comparison.diff_file(expected_unit.path, actual_unit.path)
            self.logger.log(level=self.default_logging_level, msg=diff)
