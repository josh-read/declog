import inspect
from functools import update_wrapper

from declog.utils import _get_var_name


class logged_property:
    def __init__(self, func):
        self.func = func
        update_wrapper(self, self.func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def log(key, value=None):
    """
    log(value)
    log(key, value)

    Sends value to the active logger.

    This log function takes a value and a name to reference it by.
    It then ascends the call stack to the closest BaseLogger decorated
    function, and calls its log method."""

    if value is None:
        key, value = _get_var_name(key), key

    for frame in inspect.stack():
        try:
            from .logger.base_logger import (
                BaseLogger,
            )  # import not at top of file to avoid circular import

            logger = frame.frame.f_locals["self"]
            assert isinstance(logger, BaseLogger)
            break
        except (KeyError, AssertionError):
            continue
    else:
        raise SyntaxError
    logger.log(key, value)
    return value
