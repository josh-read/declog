import tempfile

import pytest

from declog import log
from declog.logger.default_logger import DefaultLogger
from declog.database import BaseDatabase, PickleDatabase, StdOutDatabase


@pytest.mark.parametrize("database", [BaseDatabase(), StdOutDatabase()])
def test_logger_with_database(database):
    class MyLogger(DefaultLogger):
        db = database

    @MyLogger
    def my_function(a, b, c=3, d=-2):
        ab = a * b
        log(ab, "ab")
        cd = c / d
        log(None, cd)
        return ab + cd

    my_function(1, 2)


def test_logger_with_pickle_database():
    temp_file = tempfile.mktemp()

    class MyLogger(DefaultLogger):
        db = PickleDatabase(temp_file)

    @MyLogger
    def my_function(a, b, c=3, d=-2):
        ab = a * b
        log(ab, "ab")
        cd = c / d
        log(None, cd)
        return ab + cd

    my_function(1, 2)
    memory_db_data = my_function.db.data

    pickle_db = PickleDatabase(temp_file)
    pickle_db.data == memory_db_data
