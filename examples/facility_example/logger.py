from enum import Enum
from pprint import pprint

from declog.core import log
from declog.logger.base_logger import BaseLogger
from declog.database.base_database import BaseDatabase


class FacilityMachines(Enum):
    """Used to generate filepath of metadata directories. Machine number corresponds to
    folder number in /data"""

    M2 = 2
    M3 = 3


class FacilityLogger(BaseLogger):
    db = BaseDatabase()
    unique_keys = "machine shot_number function_name datetime".split()

    def build_env_dict(self):
        env_dict = super(FacilityLogger, self).build_env_dict()
        try:
            machine = self.machine
        except AttributeError:
            return env_dict
        else:
            return env_dict | {"machine": machine}

    @classmethod
    def with_machine(cls, machine: FacilityMachines):
        """Decorator factory allowing user to manually specify the machine
        without requiring it as an unused function argument"""

        def inner(func):
            flp_logger = cls(func)
            flp_logger.machine = machine
            return flp_logger

        return inner

    @staticmethod
    def get_code_version():
        """Dummy version for this test"""
        return "1.2.6"


if __name__ == "__main__":

    @FacilityLogger
    def my_processing_function(shot_number, machine, foo=False, bar=False):
        log(key="top_level_function", value="intermediate_value_1")
        double_shot_number = nested_function(shot_number)
        return double_shot_number

    def nested_function(a):
        log(key="nested_function", value="intermediate_value_1")
        return a * 2

    my_processing_function(21, FacilityMachines.M3, bar=True)
    pprint(my_processing_function.db)

    @FacilityLogger.with_machine(FacilityMachines.M3)
    def my_processing_function_specifically_for_m3(shot_number, foo=False, bar=False):
        return shot_number

    my_processing_function_specifically_for_m3(42, foo=True)

    pprint(my_processing_function_specifically_for_m3.db)
