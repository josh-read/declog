from declog.database.base_database import BaseDatabase
import pickle
import json


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
