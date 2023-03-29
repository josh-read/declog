<h1 align="center">DecLog</h1>

<p align="center">A minimal boilerplate logger for functions.</p>

<p align="center">
  <a href="https://github.com/josh-read/declog/actions/workflows/ci.yml"><img
    src="https://img.shields.io/github/actions/workflow/status/josh-read/declog/ci.yml?label=ci"
    alt="ci"
  /></a>
  <a href="https://josh-read.github.io/declog/"><img
    src="https://img.shields.io/badge/docs-mkdocs-blue" 
    alt="docs"
  /></a>
  <a href="https://pypi.org/project/declog/"><img
    src="https://img.shields.io/pypi/v/declog" 
    alt="pypi"
  /></a>
</p>

---

## Installation

To install DecLog, use [pip](https://pip.pypa.io/) to install the
latest version from PyPI.

```commandline
$ pip install declog
```

## Usage

Analysis code is typically run through a main processing function, 
which draws together library code to produce a meaningful result.

The logger is applied as a decorator to the processing function,
and captures the function arguments, intermediate values marked
with `log` and the return value.

```python
from declog import log
from declog.logger import DefaultLogger


@DefaultLogger
def my_processing_function(a, b, c=2, d=3.14):
    ab = a * b
    log(ab, 'ab')
    cd = c - d
    log(cd)
    return ab + cd


if __name__ == '__main__':
    my_processing_function(1, 5)
    print(DefaultLogger.db)

```

The BaseLogger is designed to be flexible, in the above example the base class
BaseDatabase is used which only saves logged items to a dictionary in memory.
For use as a proper logger, the database must be saved to memory. View the
[reference](https://josh-read.github.io/declog/reference/) for options or create your own backend as in the
[tutorial](https://josh-read.github.io/declog/tutorial/).

For more information on usage, check out the [about](https://josh-read.github.io/declog/about/) page or
[tutorials](https://josh-read.github.io/declog/tutorial/) in the docs.

## Contributing

All contributions are welcome! Please raise an issue or make a pull request.

