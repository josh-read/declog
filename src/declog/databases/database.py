from collections import UserDict


class Database(UserDict):

    def __missing__(self, key):
        self[key] = Database()
        return self[key]


if __name__ == '__main__':
    db = Database()
    keys = 'these are my keys'.split()

    entry = db
    for k in keys:
        entry = entry[k]

    print(db)
