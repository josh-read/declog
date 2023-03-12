from collections import UserDict


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

    def to_dict(self):
        return self._to_dict(self.data)

    @staticmethod
    def _to_dict(database):
        out = {}
        for key, value in database.items():
            if isinstance(value, BaseDatabase):
                out[key] = BaseDatabase._to_dict(value)
            else:
                out[key] = value
        return out

    @staticmethod
    def _from_dict(dictionary):
        out = BaseDatabase()
        for key, value in dictionary.items():
            if isinstance(value, dict):
                out[key] = BaseDatabase._from_dict(value)
            else:
                out[key] = value
        return out

    @classmethod
    def from_dict(cls, dictionary):
        instance = cls()
        instance.data = BaseDatabase._from_dict(dictionary)
        return instance
