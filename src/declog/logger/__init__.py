"""Loggers are classes which are applied to functions as decorators.
When the function is called, the `__call__` method of the Logger is
executed, which allows it to log the arguments supplied to the function,
in addition to other marked properties.

The Logger is separated from the database backends, allowing one logger to
be used with multiple backends and vice versa."""
import inspect
from functools import update_wrapper
from typing import Type, Any

from declog import logged_property
from declog.database import BaseDatabase, PickleDatabase
from .mixins import FunctionNameMixin, DateTimeMixin


class BaseLogger:
    """Base Logger to be subclassed by the user.

    The class attributes `db` and `unique_keys` should be set by
    subclasses."""

    db: Type[BaseDatabase] = None
    unique_keys: list[str] = None

    def __init__(self, func: callable):
        self._func = func
        update_wrapper(self, self._func)
        self.db_entry = None  # generated at call time

    def __call__(self, *args, **kwargs):
        """Evaluate wrapped function and log variables.

        Collates all the arguments and any [logged properties]() in a dictionary.
        Saves all items in the dictionary to the database `db` under a key specified
        by the class' `unique_keys` attribute."""
        # populate database with arguments and environment information
        argument_dict = self._build_arg_dict(args, kwargs)
        environment_dict = self._build_env_dict()
        call_dict = argument_dict | environment_dict
        self.db_entry = self._generate_db_entry_and_remove_keys_from_info(call_dict)
        self.db_entry |= call_dict
        # populate database with intermediate variables and result
        result = self._func(*args, *kwargs)
        self.db_entry["result"] = result
        self.db_entry = None
        try:
            self.db.write()
        except AttributeError:
            pass
        return result

    def log(self, key: str, value: Any):
        """Log the key and value to `db` under the current entry."""
        self.db_entry[key] = value

    @classmethod
    def set(cls, **kwargs):
        """Set kwargs as logged properties."""

        def inner(func):
            for key, value in kwargs.items():
                setattr(cls, key, logged_property(lambda instance: value))
            logger = cls(func)
            return logger

        return inner

    def _build_arg_dict(self, args: list[Any], kwargs: dict[str, Any]) -> dict:
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

    def _build_env_dict(self) -> dict:
        env_dict = {}
        cls = type(self)
        for obj_name in dir(self):
            try:
                obj_type = getattr(cls, obj_name)
            except AttributeError:
                obj_type = getattr(self, obj_name)
            if isinstance(obj_type, logged_property):
                obj = getattr(self, obj_name)
                env_dict[obj_name] = obj
        return env_dict

    def _generate_db_entry_and_remove_keys_from_info(self, info: dict) -> dict:
        """Returns the dictionary corresponding to the specific call entry"""
        if self.unique_keys is None:
            raise NotImplementedError
        else:
            entry = self.db
            for key in self.unique_keys:
                value = info.pop(key)
                entry = entry[value]
            return entry


class DefaultLogger(BaseLogger, FunctionNameMixin, DateTimeMixin):
    """Logger to capture function name, arguments and call time.

    A basic 'batteries included' logger. For use as a quick way to go
    from zero to logging and demonstrating how easy it is to write a
    custom Logger using mixins."""

    db = PickleDatabase
    unique_keys = ["function_name", "datetime"]
