from .base_logger import BaseLogger
from .mixins import FunctionNameMixin, DateTimeMixin


class DefaultLogger(BaseLogger, FunctionNameMixin, DateTimeMixin):
    """Logger to capture function name, arguments and call time.

    A basic 'batteries included' logger. For use as a quick way to go
    from zero to logging and demonstrating how easy it is to write a
    custom Logger using mixins."""

    unique_keys = ["function_name", "datetime"]
