import pytest

from declog import log
from declog.database import BaseDatabase, StdOutDatabase, PickleDatabase, JSONDatabase
from declog.logger import DefaultLogger

TRANSIENT_DATABASES = [BaseDatabase, StdOutDatabase]
PERSISTENT_DATABASES = [PickleDatabase, JSONDatabase]


@pytest.mark.parametrize("database", TRANSIENT_DATABASES)
def test_logger_with_database(database):
    class MyLogger(DefaultLogger):
        db = database()

    @MyLogger
    def my_function(a, b, c=3, d=-2):
        ab = a * b
        log(ab, "ab")
        cd = c / d
        log(None, cd)
        return ab + cd

    my_function(1, 2)
