import inspect

from declog.utils import _get_var_name
from typing import Any


class logged_property(property):
    pass


def log(value: Any, key: str = None):
    """Log `value` with the closest Logger.

    This function takes a value and optionally a key to call it.
    If no key is provided, the name of the variable that the value is
    assigned to is used.

    The closest logger is determined by stepping backwards through the call stack until
    a `__call__` method of a class subclassing `BaseLogger` is reached."""
    # Import outside toplevel avoids circular import
    from .logger.base_logger import BaseLogger

    if key is None:
        key = _get_var_name(value)

    # Search for closest Logger
    for frame, *_ in inspect.stack():
        try:
            (logger,) = [
                val for val in frame.f_locals.values() if isinstance(val, BaseLogger)
            ]
        except ValueError:
            pass  # move on to next frame
        else:
            logger.log(key, value)
            break
    else:
        raise SyntaxError("No logger found in the call stack.")
