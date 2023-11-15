import difflib
import os.path
import pathlib
from typing import *

from goldenfile.comparison import cmp_file, diff_file
from goldenfile.exception import GoldenfileError

from goldenfile.model import ExecutedTest, TestSuiteExecutionResult
from goldenfile.reporters.base_reporter import BaseReporter
from termcolor import cprint, colored


class HtmlDiffReporter(BaseReporter):
    # TODO nikolay rulev: rewrite on https://github.com/rtfpessoa/diff2html
    @staticmethod
    def show_diff(result: TestSuiteExecutionResult) -> None:
        def print_failed_tests_diff(test: ExecutedTest) -> List[str]:
            checks = [
                ("stdout", test.test.golden_stdout, test.output.actual_stdout),
                ("stderr", test.test.golden_stderr, test.output.actual_stderr),
                # TODO
                # ("generated file", test.test.golden_generated_file, test.output.actual_generated_file),
            ]
            diffs = []
            for name, golden, actual in checks:
                if golden is None:
                    continue
                if not cmp_file(golden, actual):
                    diff = HtmlDiffReporter._html_diff_table(golden, actual)
                    diffs.append(diff)
            return diffs

        checks_results = []
        result_html = ""
        for t in result.failed:
            res = print_failed_tests_diff(t)
            checks_results.append((t.test.name, res))
        for (t, diffs) in checks_results:
            result_html += f"<h2>{t}</h2>"
            for d in diffs:
                result_html += d

        print(_HTML_HEADER + result_html + _HTML_BOTTOM, file=open("failed_tests_diffs.html", "w"))
        HtmlDiffReporter.print_passed_tests_colored(result)
        HtmlDiffReporter.print_skipped_tests_colored(result)
        HtmlDiffReporter.print_failed_tests_colored(result)

        print("See diff in html at failed_tests_diffs.html")
        HtmlDiffReporter.print_summary_colored(result)

    @staticmethod
    def _html_diff_table(golden_path, actual_path):
        if not golden_path.is_file():
            raise GoldenfileError(f"Incorrect file: {golden_path}")

        if not actual_path.is_file():
            raise GoldenfileError(f"Incorrect file: {actual_path}")

        golden_content: str = golden_path.read_text(encoding="utf-8")
        actual_content: str = actual_path.read_text(encoding="utf-8")

        # print(golden_content)
        # print(actual_content)
        difference = difflib.HtmlDiff(
            tabsize=4,
            # wrapcolumn=40,
        )

        return difference.make_table(fromlines=golden_content.splitlines(),
                                     tolines=actual_content.splitlines(),
                                     fromdesc=f"Expected {golden_path}",
                                     todesc=f"Actual {actual_path}",
                                     context=True,
                                     # numlines=5,
                                     )



_HTML_HEADER = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=utf-8" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style>
</head>
<body>
"""


_HTML_BOTTOM = """
</body>
</html>
"""