from enum import Enum

from pprint import pprint
from pathlib import Path

from declog.core import log, logged_property
from declog.logger import BaseLogger
from declog.database import JSONDatabase, PersistentDatabase
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
        print(item)
        if isinstance(item, FacilityMachines):
            return self.dbs[item]
        else:
            raise TypeError(
                "The first key when using the FacilityDatabase must be a machine."
            )

    def __setitem__(self, key, value):
        print(key, value)
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


if __name__ == "__main__":
    # set up the directory structure
    for path in FacilityDatabase.gen_db_paths().values():
        path.parent.mkdir(parents=True, exist_ok=True)

    @FacilityLogger
    def my_processing_function(shot_number, machine, foo=False, bar=False):
        log(value="intermediate_value_1", key="top_level_function")
        double_shot_number = nested_function(shot_number)
        return double_shot_number

    def nested_function(a):
        log(value="intermediate_value_2", key="nested_function")
        return a * 2

    my_processing_function(21, FacilityMachines.M2, bar=True)
    pprint(my_processing_function.db)

    @FacilityLogger.set(machine=FacilityMachines.M3)
    def my_processing_function_specifically_for_m3(shot_number, foo=False, bar=False):
        return shot_number

    my_processing_function_specifically_for_m3(42, foo=True)

    pprint(my_processing_function_specifically_for_m3.db)
