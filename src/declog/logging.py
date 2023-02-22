import inspect
from datetime import datetime
from functools import update_wrapper
from getpass import getuser


class logged_property:
    def __init__(self, func):
        self.func = func
        update_wrapper(self, self.func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Logger:
    """Logger class to be subclassed"""

    db = None
    unique_keys: list[str] = None

    def __init__(self, func):
        self._func = func
        update_wrapper(self, self._func)
        self.db_entry = None  # generated at call time

    def generate_db_entry_and_remove_keys_from_info(self, info: dict):
        """Returns the dictionary corresponding to the specific call entry"""
        if self.unique_keys is None:
            raise NotImplementedError
        else:
            entry = self.db
            for key in self.unique_keys:
                value = info.pop(key)
                entry = entry[value]
            return entry

    def __call__(self, *args, **kwargs):
        """The call method is typically overridden in child classes."""
        # populate database with arguments and environment information
        argument_dict = self.build_arg_dict(args, kwargs)
        environment_dict = self.build_env_dict()
        call_dict = argument_dict | environment_dict
        self.db_entry = self.generate_db_entry_and_remove_keys_from_info(call_dict)
        self.db_entry |= call_dict
        # populate database with intermediate variables and result
        result = self._func(*args, *kwargs)
        self.db_entry["result"] = result
        self.db_entry = None
        return result

    def log(self, key, value):
        self.db_entry[key] = value

    def build_arg_dict(self, args, kwargs):
        positional_args = {
            k: v for k, v in zip(inspect.signature(self._func).parameters, args)
        }
        default_args = {
            k: v.default
            for k, v in inspect.signature(self._func).parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        keyword_args = (
            default_args | kwargs
        )  # update defaults with supplied keyword arguments
        return positional_args | keyword_args

    def build_env_dict(self):
        env_dict = {}
        for obj_name in dir(self):
            obj = getattr(self, obj_name)
            if isinstance(obj, logged_property):
                env_dict[obj_name] = obj(self)
        return env_dict

    @logged_property
    def function_name(self):
        return self._func.__name__

    @logged_property
    def datetime(self):
        return str(datetime.now())

    @logged_property
    def user(self):
        return getuser()


def _get_var_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    (var_name,) = [name for name, val in callers_local_vars if val is var]
    return var_name


def log(key, value=None):
    """
    log(value)
    log(key, value)

    Sends value to the active logger.

    This log function takes a value and a name to reference it by.
    It then ascends the call stack to the closest Logger decorated
    function, and calls its log method."""

    if value is None:
        key, value = _get_var_name(key), key

    for frame in inspect.stack():
        try:
            logger = frame.frame.f_locals["self"]
            assert isinstance(logger, Logger)
            break
        except (KeyError, AssertionError):
            continue
    else:
        raise SyntaxError
    logger.log(key, value)
    return value
