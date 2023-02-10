from collections import UserDict


class Database(UserDict):

    def __init__(self, root=None):
        """root is not meant to be used by the user"""
        if root is None:
            self.root = self
        else:
            self.root = root
        super().__init__()

    def __missing__(self, key):
        self[key] = self.__class__(root=self.root)
        return self[key]


def test_database_default_keys():
    db = Database()
    my_dict = {
        'a': 'b',
        'c': 'd',
    }

    entry = db
    for k in my_dict.keys():
        value = my_dict[k]
        entry = entry[value]

    print(db)


def test_with_logger():
    from declog.loggers.logger import Logger, log

    class MyLogger(Logger):
        db = Database()
        unique_keys = 'function_name datetime'.split()

    @MyLogger
    def my_function(a, b, c=3, d=-2):
        ab = a * b
        log('ab', ab)
        cd = c / d
        log(cd)
        return ab + cd

    my_function(1, 2)
    print(my_function.db)


if __name__ == '__main__':
    test_database_default_keys()
    test_with_logger()
