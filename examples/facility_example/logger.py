from enum import Enum
from pprint import pprint

from declog.core import log, logged_property
from declog.logger.base_logger import BaseLogger
from declog.database import BaseDatabase
from declog.logger.mixins import FunctionNameMixin, DateTimeMixin, UserMixin


class FacilityMachines(Enum):
    """Used to generate filepath of metadata directories. Machine number corresponds to
    folder number in /data"""

    M2 = 2
    M3 = 3


class FacilityLogger(BaseLogger, FunctionNameMixin, DateTimeMixin, UserMixin):
    db = BaseDatabase()
    unique_keys = "machine shot_number function_name datetime".split()

    @logged_property
    def version(self):
        """Dummy version for this test"""
        return "1.2.6"


if __name__ == "__main__":

    @FacilityLogger
    def my_processing_function(shot_number, machine, foo=False, bar=False):
        log(value="intermediate_value_1", key="top_level_function")
        double_shot_number = nested_function(shot_number)
        return double_shot_number

    def nested_function(a):
        log(value="intermediate_value_2", key="nested_function")
        return a * 2

    my_processing_function(21, FacilityMachines.M3, bar=True)
    pprint(my_processing_function.db)

    @FacilityLogger.set(machine=FacilityMachines.M2)
    def my_processing_function_specifically_for_m3(shot_number, foo=False, bar=False):
        return shot_number

    my_processing_function_specifically_for_m3(42, foo=True)

    pprint(my_processing_function_specifically_for_m3.db)
