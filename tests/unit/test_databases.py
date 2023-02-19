from declog.database.database import Database
from declog.database.std_out_database import StdOutDatabase
from declog.database.pickle_database import PickleDatabase
import tempfile


class TestDatabase:
    @staticmethod
    def get_db():
        return Database()

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
