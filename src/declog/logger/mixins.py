from getpass import getuser
from datetime import datetime

from ..core import logged_property


class FunctionNameMixin:
    @logged_property
    def function_name(self):
        return self._func.__name__


class DateTimeMixin:
    @logged_property
    def datetime(self):
        return str(datetime.now())


class UserMixin:
    @logged_property
    def user(self):
        return getuser()
