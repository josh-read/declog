from declog.debug import StdOutLogger
from declog.logger import Logger, log
from importlib.metadata import version, PackageNotFoundError


__all__ = ["Logger", "log", "StdOutLogger"]

try:
    __version__ = version("declog")
except PackageNotFoundError:
    pass
else:
    __all__.append("__version__")
