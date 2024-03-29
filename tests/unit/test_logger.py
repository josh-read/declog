import pytest

from declog.database import BaseDatabase
from declog.logger import BaseLogger
from declog.logger.mixins import FunctionNameMixin


@pytest.fixture()
def logger():
    class MyLogger(BaseLogger, FunctionNameMixin):
        db = BaseDatabase()
        unique_keys = ["function_name"]

    return MyLogger


def test_nested_logger(logger):
    @logger
    def my_function(x):
        return my_function_inner(x)

    @logger
    def my_function_inner(x):
        return x

    my_function(1)

    assert logger.db.data == {
        "my_function": {"x": 1, "result": 1},
        "my_function_inner": {"x": 1, "result": 1},
    }


def test_argument_capture(logger):
    @logger
    def my_function(a, b, c=3, d=-1):
        return a * b * d - c

    my_function(1, 2, d=4)

    assert logger.db == {"my_function": {"a": 1, "b": 2, "c": 3, "d": 4, "result": 5}}


def test_duplicate_entries(logger):
    """Duplicate keys are overwritten - highlights the importance of choosing
    non-conflicting keys"""

    @logger
    def my_function(x):
        return x

    my_function(0)
    my_function(1)
    my_function(2)

    assert logger.db == {"my_function": {"x": 2, "result": 2}}


def test_set_method(logger):
    @logger
    def my_func_1(number):
        pass

    @logger.set(number=42)
    def my_func_2():
        pass

    @logger
    def my_func_3(number):
        pass

    my_func_1(0)
    my_func_2()
    my_func_3(0)

    assert logger.db.data == {
        "my_func_1": {"number": 0, "result": None},
        "my_func_2": {"number": 42, "result": None},
        "my_func_3": {"number": 0, "result": None},
    }
