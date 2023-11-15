from pathlib import Path
import sys

file = Path(sys.argv[1])
print("Writing to", file)
file.write_text("This is written to a file")
