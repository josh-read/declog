import shelve
import tempfile
from declog.loggers.logger import Logger
from declog.databases.database import Database


class ShelveDatabase(shelve.DbfilenameShelf, Database):

    def __init__(self, filename):
        Database.__init__(self)
        shelve.DbfilenameShelf.__init__(self, filename, writeback=True)


if __name__ == '__main__':

    temp_file = tempfile.mktemp()

    shelve_database = ShelveDatabase(temp_file)

    with shelve_database as db:
        print(db)
        db['hi'] = 'hello'
        print(db)
    print('done')

    with shelve.open(temp_file) as db:
        print(db.dict)
        print(db['hi'])
