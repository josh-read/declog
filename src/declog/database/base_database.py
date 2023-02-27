from collections import UserDict


class BaseDatabase(UserDict):
    def __init__(self, root=None):
        """root is not meant to be used by the user"""
        if root is None:
            self.root = self
        else:
            self.root = root
        super().__init__()

    def __missing__(self, key):
        self[key] = BaseDatabase(root=self.root)
        return self[key]
