Requirements
============

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

`000_test/000_test.fileoutput`

```
(temppath) -> compiler.exe -o {temppath}
```
