import inspect
from typing import Any

from declog.exceptions import ParentLoggerNotFoundError
from declog.utils import _get_var_name


class logged_property(property):
    """Marks a property to be logged.

    Thin wrapper around a standard property. Used in a logger class when the property is
    to be logged each time the wrapped function is called.

    Example:
        >>> from declog.logger import BaseLogger
        >>> from declog.database import BaseDatabase
        ...
        >>> class MyLogger(BaseLogger):
        ...     db = BaseDatabase()
        ...     unique_keys = ['function_name', 'counter']
        ...
        ...     def __init__(self, func):
        ...         super().__init__(func)
        ...         self._counter = 0
        ...
        ...     @logged_property
        ...     def function_name(self):
        ...         return self._func.__name__
        ...
        ...     @logged_property
        ...     def counter(self):
        ...         n = self._counter
        ...         self._counter += 1
        ...         return n
        ...
        ...     @logged_property
        ...     def foo(self):
        ...         return 'bar'
        ...
        >>> @MyLogger
        ... def my_function():
        ...     pass
        ...
        >>> my_function()
        >>> my_function()
        >>> my_function()
        >>> MyLogger.db
        {'my_function': \
{0: {'foo': 'bar', 'result': None}, \
1: {'foo': 'bar', 'result': None}, \
2: {'foo': 'bar', 'result': None}}}
    """


def log(value: Any, key: str = None):
    """Log `value` with the closest Logger.

    This function takes a value and optionally a key to call it.
    If no key is provided, the name of the variable that the value is
    assigned to is used.

    The closest logger is determined by stepping backwards through the call stack until
    a `__call__` method of a class subclassing `BaseLogger` is reached."""
    # Import outside toplevel avoids circular import
    from declog.logger import BaseLogger

    if key is None:
        key = _get_var_name(value, n=2)

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
        raise ParentLoggerNotFoundError("No logger found in the call stack.")
