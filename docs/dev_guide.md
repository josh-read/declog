# Environment setup

To get set up, run the following:

```commandline
$ git clone https://github.com/josh-read/declog.git
$ cd declog
$ python3.11 venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip
$ python3 -m pip install -e ".[dev]"
$ pre-commit install
```

This will download the source code from git, create a virtual environment,
install a live (editable version) the package along with the development
dependencies, and install the pre-commit hooks, which ensure the code conforms
with the project code style (black and flake8).