import re
import runpy
import tempfile
from pathlib import Path

import pytest


def discover_codeblocks():
    """Get a generator of every python file in the examples directory."""
    docs_path = Path("docs")
    markdown_files = docs_path.glob("**/*.md")
    for file in markdown_files:
        with open(file, "r") as f:
            text = f.read()
        codeblocks = re.findall("```python(.*)```", text, re.DOTALL)
        for code in codeblocks:
            yield file, code


@pytest.mark.parametrize("file, code", discover_codeblocks())
def test_codeblocks(file, code):
    temp_file = tempfile.mktemp()
    with open(temp_file, "w") as f:
        f.write(code)
    runpy.run_path(temp_file, run_name="__main__")
