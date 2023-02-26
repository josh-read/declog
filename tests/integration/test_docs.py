import re
from pathlib import Path


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


if __name__ == "__main__":
    for file, code in discover_codeblocks():
        exec(code)
