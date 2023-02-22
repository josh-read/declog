from .base_logger import BaseLogger
from .mixins import FunctionName, DateTime


class DefaultLogger(BaseLogger, FunctionName, DateTime):
    unique_keys = ["function_name", "datetime"]
