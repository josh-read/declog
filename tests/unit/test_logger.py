from declog.logger import BaseLogger
from declog.logger.mixins import FunctionNameMixin
from declog.database import BaseDatabase


def test_nested_logger():
    class MyLogger(BaseLogger, FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    @MyLogger
    def my_function(x):
        return my_function_inner(x)

    @MyLogger
    def my_function_inner(x):
        return x

    my_function(1)

    assert MyLogger.db.data == {
        "my_function": {"x": 1, "result": 1},
        "my_function_inner": {"x": 1, "result": 1},
    }


def test_argument_capture():
    class MyLogger(BaseLogger, FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    @MyLogger
    def my_function(a, b, c=3, d=-1):
        return a * b * d - c

    my_function(1, 2, d=4)

    assert MyLogger.db == {"my_function": {"a": 1, "b": 2, "c": 3, "d": 4, "result": 5}}


def test_duplicate_entries():
    """Duplicate keys are overwritten - highlights the importance of choosing
    non-conflicting keys"""

    class MyLogger(BaseLogger, FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    @MyLogger
    def my_function(x):
        return x

    my_function(0)
    my_function(1)
    my_function(2)

    assert MyLogger.db == {"my_function": {"x": 2, "result": 2}}


def test_set_method():
    class MyLogger(BaseLogger, FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name", "number"]

    @MyLogger
    def my_func_1(number):
        return number

    @MyLogger.set(number=42)
    def my_func_2():
        pass

    @MyLogger
    def my_func_3(number):
        return {"hello": "world"}

    my_func_1(2)
    my_func_1(3)
    my_func_2()
    my_func_3(None)

    assert MyLogger.db.data == {
        "my_func_1": {2: {"result": 2}, 3: {"result": 3}},
        "my_func_2": {42: {"result": None}},
        "my_func_3": {None: {"result": {"hello": "world"}}},
    }
