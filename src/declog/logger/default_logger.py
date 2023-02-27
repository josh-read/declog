from .base_logger import BaseLogger
from .mixins import FunctionNameMixin, DateTimeMixin


class DefaultLogger(BaseLogger, FunctionNameMixin, DateTimeMixin):
    unique_keys = ["function_name", "datetime"]
