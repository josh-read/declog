"""Drawback of pickle is the whole thing must be read
from path so for a big database this will be slow.

Upside is native python objects can be stored so absolutely
anything can be logged, while for others it is more limited."""

import tempfile
from declog.loggers.logger import Logger, log
from declog.databases.database import Database
import pickle


class PickleDatabase(Database):

    def __init__(self, path, root=None):
        self.path = path
        super().__init__(root=root)

    def __enter__(self):
        try:
            with open(self.path, 'rb+') as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            pass
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self.path, 'wb') as f:
            pickle.dump(self.data, f)


def test_with_logger():
    temp_file = tempfile.mktemp()

    with PickleDatabase(temp_file) as pdb:
        class MyLogger(Logger):
            db = pdb
            unique_keys = 'function_name datetime'.split()

        @MyLogger
        def my_function(a, b, c=3, d=-2):
            ab = a * b
            log('ab', ab)
            cd = c / d
            log(cd)
            return ab + cd

        my_function(1, 2)

    pickle_db = PickleDatabase(temp_file)
    with pickle_db:
        print(pickle_db.data)
        print(pickle_db['my_function'])


if __name__ == '__main__':
    test_with_logger()
