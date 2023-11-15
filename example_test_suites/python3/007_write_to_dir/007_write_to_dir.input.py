from pathlib import Path
import sys

file = Path(sys.argv[1])
file.mkdir()
(file / "a.txt").write_text("Text")
