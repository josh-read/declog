from declog import log
from declog.logger import BaseLogger, mixins
from declog.database import BaseDatabase


def test_log_in_nested_function():
    class MyLogger(BaseLogger, mixins.FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    @MyLogger
    def my_function():
        my_function_inner()

    def my_function_inner():
        log("value", "key")

    my_function()

    assert MyLogger.db == {"my_function": {"key": "value", "result": None}}


def test_log_with_key():
    class MyLogger(BaseLogger, mixins.FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    @MyLogger
    def my_function():
        log("value", "key")

    my_function()

    assert MyLogger.db == {"my_function": {"key": "value", "result": None}}


def test_log_without_key():
    class MyLogger(BaseLogger, mixins.FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    @MyLogger
    def my_function():
        key = "value"
        log(key)

    my_function()

    assert MyLogger.db == {"my_function": {"key": "value", "result": None}}
