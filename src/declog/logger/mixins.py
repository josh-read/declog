"""Collection of classes containing commonly used logged properties.

These are used as mixins to save time making custom loggers. For an example
of this in action, take a look at the DefaultLogger."""


from getpass import getuser
from datetime import datetime

from ..core import logged_property


class FunctionNameMixin:
    @logged_property
    def function_name(self) -> str:
        """Name of the wrapped function."""
        return self._func.__name__


class DateTimeMixin:
    @logged_property
    def datetime(self) -> str:
        """The time and date."""
        return str(datetime.now())


class UserMixin:
    @logged_property
    def user(self) -> str:
        """The current user."""
        return getuser()
