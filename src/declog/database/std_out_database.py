from declog.database.base_database import BaseDatabase


class StdOutDatabase(BaseDatabase):
    """Database which prints itself every time a value gets logged."""

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        print(self.root)

    def __missing__(self, key):
        self[key] = StdOutDatabase(root=self.root)
        return self[key]
