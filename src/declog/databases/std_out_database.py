from declog.databases.database import Database


class StdOutDatabase(Database):

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        print(self.root)


def test_with_logger():
    from declog.loggers.logger import Logger, log

    class MyLogger(Logger):
        db = StdOutDatabase()
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
    test_with_logger()
