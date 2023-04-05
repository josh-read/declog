from declog.logger import BaseLogger
from declog.logger.mixins import FunctionNameMixin
from declog.database import BaseDatabase


def test_nested_logger():
    assert False


def test_argument_capture():
    assert False


def test_duplicate_entries():
    assert False


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
