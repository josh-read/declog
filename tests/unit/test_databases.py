import tempfile

import pytest

from declog.database import BaseDatabase, PickleDatabase, StdOutDatabase, JSONDatabase

TRANSIENT_DATABASES = [BaseDatabase, StdOutDatabase]
PERSISTENT_DATABASES = [PickleDatabase, JSONDatabase]


class TestDatabase:
    @staticmethod
    def get_db():
        return BaseDatabase()

    def test_getitem_simple(self):
        db = self.get_db()
        db["foo"]
        assert db == {"foo": {}}

    def test_getitem_chained(self):
        db = self.get_db()
        db["foo"]["bar"]["baz"]
        assert db == {"foo": {"bar": {"baz": {}}}}

    def test_setitem_simple(self):
        db = self.get_db()
        db["foo"] = 42
        assert db == {"foo": 42}

    def test_setitem_chained(self):
        db = self.get_db()
        db["foo"]["bar"]["baz"] = 42
        assert db == {"foo": {"bar": {"baz": 42}}}


class TestStdOutDatabase(TestDatabase):
    @staticmethod
    def get_db():
        return StdOutDatabase()


class TestPickleDatabase(TestDatabase):
    @staticmethod
    def get_db():
        temp_file = tempfile.mktemp()
        return PickleDatabase(temp_file)


class TestJSONDatabase(TestDatabase):
    @staticmethod
    def get_db():
        temp_file = tempfile.mktemp()
        return JSONDatabase(temp_file)


@pytest.mark.parametrize("database", PERSISTENT_DATABASES)
def test_persistent_database_recall(database):
    temp_file = tempfile.mktemp()

    memory_db = database(temp_file)
    memory_db["hi"] = "hello"
    memory_db.write()

    storage_db = database(temp_file)
    assert storage_db.data == memory_db.data
