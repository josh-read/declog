from declog.database.base_database import BaseDatabase


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
