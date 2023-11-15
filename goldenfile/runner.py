from abc import ABC, abstractmethod
from pathlib import Path
import shutil
import subprocess
from typing import Callable, Sequence
from goldenfile.constants import GENERATED_FILE_SUFFIX, STDERR_SUFFIX, STDOUT_SUFFIX
from goldenfile.model import ExecutedTest, Runner, Test, TestOutput

TMP_DIR = Path("temp")


class ShellCommand(ABC):
    @abstractmethod
    def make_command(self, *, input_path: Path, output_path: Path) -> Sequence[str]:
        ...


def run_tests_in_shell(
        tests: Sequence[Test],
        command: ShellCommand,
) -> Sequence[ExecutedTest]:
    def run_command(cmd: Sequence[str], stdout_path: Path, stderr_path: Path):
        # This function is written by ChatGPT
        with open(stdout_path, "w") as stdout_file, open(
                stderr_path, "w"
        ) as stderr_file:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout_file.write(result.stdout.decode())
            stderr_file.write(result.stderr.decode())

    def run_test(test: Test) -> ExecutedTest:
        test_dir = TMP_DIR / test.name
        test_dir.mkdir()
        test_output_path = test_dir / (test.name + GENERATED_FILE_SUFFIX)
        test_stdout_path = test_dir / (test.name + STDOUT_SUFFIX)
        test_stderr_path = test_dir / (test.name + STDERR_SUFFIX)
        assert test.input is not None, test.name
        run_command(
            cmd=command.make_command(input_path=test.input, output_path=test_output_path),
            stdout_path=test_stdout_path,
            stderr_path=test_stderr_path,
        )
        return ExecutedTest(
            test=test,
            output=TestOutput(
                actual_stdout=test_stdout_path,
                actual_stderr=test_stderr_path,
                actual_generated_file=test_output_path,
            ),
        )

    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True)

    return [run_test(test) for test in tests]


def shell_runner(cmd: ShellCommand) -> Runner:
    return lambda tests: run_tests_in_shell(tests, cmd)
