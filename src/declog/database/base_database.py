from collections import UserDict


class BaseDatabase(UserDict):
    def __init__(self, root=None):
        """Base class for Databases to be used with declog Loggers.

        When a key which does not yet exist is accessed, an empty database
        is created as the value for that key. This enables a nested keys to
        be used. All Database types must have this functionality in order
        for them to be used by a declog Logger."""
        if root is None:
            self.root = self
        else:
            self.root = root
        super().__init__()

    def __missing__(self, key):
        self[key] = BaseDatabase(root=self.root)
        return self[key]
