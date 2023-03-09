from declog.database.base_database import BaseDatabase
import pickle


class PickleDatabase(BaseDatabase):
    """BaseDatabase which gets written to a pickle file.

    Drawback of pickle is the whole thing must be read
    from path so for a big database this will be slow.

    Upside is native python objects can be stored so absolutely
    anything can be logged, while for others it is more limited."""

    def __init__(self, path, root=None):
        self.path = path
        super().__init__(root=root)

    def __enter__(self):
        try:
            with open(self.path, "rb+") as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.path, "wb") as f:
            pickle.dump(self.data, f)
