import inspect
from functools import update_wrapper


class Logger:
    """Logger class to be subclassed"""

    def __init__(self, func):
        self._func = func
        update_wrapper(self, self._func)

    def __call__(self, *args, **kwargs):
        """The call method is typically overridden in child classes.
        """
        return self._func(*args, *kwargs)

    def log(self, key, value):
        pass

    def build_arg_dict(self, args, kwargs):
        positional_args = {k: v for k, v in zip(inspect.signature(self._func).parameters, args)}
        default_args = {k: v.default for k, v in inspect.signature(self._func).parameters.items() if
                        v.default is not inspect.Parameter.empty}
        keyword_args = default_args | kwargs  # update defaults with supplied keyword arguments
        return positional_args | keyword_args


def get_var_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    var_name, = [name for name, val in callers_local_vars if val is var]
    return var_name


def log(key, value=None):
    """
    log(value)
    log(key, value)

    This log function takes a value and a name to reference it by. It then ascends the call stack to the closest
    Logger decorated function, and calls its log method."""

    if value is None:
        key, value = get_var_name(key), key

    for frame in inspect.stack():
        try:
            logger = frame.frame.f_locals['self']
            assert isinstance(logger, Logger)
            break
        except (KeyError, AssertionError):
            continue
    else:
        raise SyntaxError
    logger.log(key, value)
    return value
