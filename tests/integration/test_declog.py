import tempfile

import pytest

from declog import BaseLogger, log
from declog.database import Database, PickleDatabase, StdOutDatabase


@pytest.mark.parametrize("database", [Database(), StdOutDatabase()])
def test_logger_with_database(database):
    class MyLogger(BaseLogger):
        db = database
        unique_keys = "function_name datetime".split()

    @MyLogger
    def my_function(a, b, c=3, d=-2):
        ab = a * b
        log("ab", ab)
        cd = c / d
        log(cd)
        return ab + cd

    my_function(1, 2)


def test_logger_with_pickle_database():
    temp_file = tempfile.mktemp()

    with PickleDatabase(temp_file) as pdb:

        class MyLogger(BaseLogger):
            db = pdb
            unique_keys = "function_name datetime".split()

        @MyLogger
        def my_function(a, b, c=3, d=-2):
            ab = a * b
            log("ab", ab)
            cd = c / d
            log(cd)
            return ab + cd

        my_function(1, 2)
        memory_db_data = my_function.db.data

    pickle_db = PickleDatabase(temp_file)
    with pickle_db:
        assert pickle_db.data == memory_db_data
