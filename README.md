# Goldenfile

> A framework for golden-file testing

## Описание

Golden file тестирование --- метод (обычно сквозного) тестирования, при котором выход программы проверяется на совпадение с эталонным "золотым" выводом (goldenfile).

Данный вид тестирования очень актуален при разработке компиляторов, трансляторов, интерпретаторов или любых анализаторов и преобразователей исходного кода. Он позволяет полуавтоматически покрывать тестами важную логику программы, не залезая в ее внутренности. Таким образом, данные тесты не являются мертвым грузом при рефакторинге.

Текущие инструмента либо реализованы для конкретного языка программирования(https://pkg.go.dev/gotest.tools/v3/golden, https://github.com/sebdah/goldie), либо имеют удобный интерфейс запуска, но больше не поддерживаются (https://github.com/aiiie/cram). Никакой инструмент, из тех которых я знаю, не поддерживает голден директории.

Пользоваться таким инструментом должно быть довольно просто. На диске (в папке tests) хранятся файлы со входными данными и для каждого такого файла хранится эталонный goldenfile. Инструмент запускает тестируемую программу (допустим, интерпретатор), передавая ей каждый файл со входными данными и сверает выход (результат интерпретации) с голден файлом.

## Requirements

_Program_ - the program under test

**UI requirements**

* Command-line interface
    * Can be used out-of-the-box
    * Can be configured with YAML
* Integration with pytest
    * Can be used out-of-the-box
    * Can be configured
* Programmatic Python API
    * Allows full customization
* Integration with some other non-Python build system (e.g. Gradle)
* Cram-like interface

**Input requirements**

* Program input may be text or files/directories from disk
* Supports global and per-test config (see below)

**Output requirements**

* Program output may be stdout and stderr or files/directories on disk
* Can automatically update golden files (and directories)
* Can print diffs (or write into `.diff` files)
* Can generate `.err` files

**Configuration requirements**

* Programmatic config
    * Modular design
    * Users can define their components
    * Users can programmatically (in Python) define custom testing frameworks with custom and official components
    * Use case: the user sets up an entire golden-file testing system for their C/Haskell/OCaml/or whatever project in a single file, and runs it with `python3 test_goldenfile.py`
* Config for CLI interface
    * How to run the binary?
    * How to pass parameters
    * ...
* Default global config format for pytest integration
    * Users can define their own config formats with the Python API
* Per-test config
    * An additional config for each test
    * Can override some options from the global config
    * Defines additional options
    * Users can define their own config formats with the Python API
        * Users can choose to lower their config formats into our config format

* mode: stdout stderr filesystem

000_test/000_test.fileoutput

(temppath) -> compiler.exe -o {temppath}

----------------------
Design

Test:
    name
    tags
    input
    golden_stdout
    golden_stderr
    golden_file_output

Result = (Test, TestOutput)

TestOutput:
    actual_stdout
    actual_stderr
    actual_file_output

Pipeline:: () -> unit = TestDiscovery |> Runner |> List[Exporter]

Framework.run(pipelines: List[Pipeline])

Test Discovery:: ((testtags: List[tag]) -> bool) -> List[Test]
Runner:: (List[Test]) -> List[Result]
Exporter:: List[Result] -> unit

1. Comparison API
2. Test Discovery
3. Runner
4. UpdateExporter
5. DiffExporter

* BeforeAll, AfterAll, BeforeEach, AfterEach

---

## Dependencies

* [pyenv](https://github.com/pyenv/pyenv)
* [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

## Toolchain

Installation:

```shell
pyenv install 3.11
pyenv local 3.11
poetry env use $(pyenv which python)
poetry install
```

Enter into Poetry virtual environment:

```shell
poetry shell
```

## Tests

```shell
pytest
```
