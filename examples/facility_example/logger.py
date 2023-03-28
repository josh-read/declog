from enum import Enum
from pathlib import Path

from declog.core import logged_property
from declog.database import JSONDatabase, PersistentDatabase
from declog.logger import BaseLogger
from declog.logger.mixins import FunctionNameMixin, DateTimeMixin, UserMixin


class FacilityMachines(Enum):
    """Used to generate filepath of metadata directories. Machine number corresponds to
    folder number in /data"""

    M2 = 2
    M3 = 3


class FacilityDatabase(PersistentDatabase):
    def __init__(self):
        db_paths = self.gen_db_paths()
        self.dbs = {k: JSONDatabase(v) for k, v in db_paths.items()}

    def __getitem__(self, item):
        if isinstance(item, FacilityMachines):
            return self.dbs[item]
        else:
            raise TypeError(
                "The first key when using the FacilityDatabase must be a machine."
            )

    def __setitem__(self, key, value):
        if isinstance(key, FacilityMachines):
            self.dbs[key] = value

    def __repr__(self):
        print_dict = {}
        for machine, db in self.dbs.items():
            print_dict[machine] = db
        return repr(print_dict)

    def write(self):
        for db in self.dbs.values():
            db.write()

    @staticmethod
    def gen_db_paths():
        machine_databases = {}
        data_path = Path(__file__).parent / "data"
        for machine in FacilityMachines:
            db_path = Path(f"{machine.value:02d}_{machine.name}/metadata/shot_db.json")
            machine_databases[machine] = data_path / db_path
        return machine_databases


class FacilityLogger(BaseLogger, FunctionNameMixin, DateTimeMixin, UserMixin):
    db = FacilityDatabase()
    unique_keys = "machine shot_number function_name datetime".split()

    @logged_property
    def version(self):
        """Dummy version for this test"""
        return "1.2.6"
