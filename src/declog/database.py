import json
import pickle
from collections import UserDict
from typing import MutableMapping


class BaseDatabase(UserDict):
    """Base class for Databases to be used with declog Loggers.

    When a key which does not yet exist is accessed, an empty database
    is created as the value for that key. This enables a nested keys to
    be used. All Database types must have this functionality in order
    for them to be used by a declog Logger."""

    def __init__(self, writeback=False):
        super(BaseDatabase, self).__init__()
        self.writeback = writeback

    def __setitem__(self, key, value):
        super(BaseDatabase, self).__setitem__(key, value)
        if self.writeback:
            self.write()

    def __missing__(self, key):
        self[key] = BaseDatabase()
        return self[key]

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError

    @staticmethod
    def cast(mutable_mapping, new_type):
        out = new_type()
        for key, value in mutable_mapping.items():
            if isinstance(value, MutableMapping):
                out[key] = BaseDatabase.cast(value, new_type)
            else:
                out[key] = value
        return out

    def to_dict(self):
        return BaseDatabase.cast(self.data, dict)

    @classmethod
    def from_dict(cls, dictionary):
        instance = cls()
        instance.data = BaseDatabase.cast(dictionary, BaseDatabase)
        return instance


class StdOutDatabase(BaseDatabase):
    """Database which prints itself every time a value gets logged."""

    def __init__(self, _root=None):
        super(StdOutDatabase, self).__init__(writeback=True)
        if _root is None:
            self.root = self
        else:
            self.root = _root

    def __missing__(self, key):
        self[key] = StdOutDatabase(_root=self.root)
        return self[key]

    def write(self):
        print(self.root)


class PersistentDatabase(BaseDatabase):
    def __init__(self, path):
        self.path = path
        super().__init__()
        self.read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write()


class PickleDatabase(PersistentDatabase):
    """BaseDatabase which gets written to a pickle file.

    Drawback of pickle is the whole thing must be read
    from path so for a big database this will be slow.

    Upside is native python objects can be stored so absolutely
    anything can be logged, while for others it is more limited."""

    def read(self):
        try:
            with open(self.path, "rb") as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            pass

    def write(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.data, f)


class JSONDatabase(PersistentDatabase):
    def read(self):
        try:
            with open(self.path, "r") as f:
                self.data = BaseDatabase.from_dict(json.load(f))
        except FileNotFoundError:
            pass

    def write(self):
        with open(self.path, "w") as f:
            json.dump(self.to_dict(), f)
