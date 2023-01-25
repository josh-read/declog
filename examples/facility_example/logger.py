from datetime import datetime
from enum import Enum
from getpass import getuser

from declog import Logger, log


class FacilityMachines(Enum):
    """Used to generate filepath of metadata directories. Machine number corresponds to folder number in /data"""
    M2 = 2
    M3 = 3


class FacilityLogger(Logger):

    def __init__(self, func):
        func.logger = self  # normally unnescessary, but this allows us to open up the logger after all the logging is done to look inside
        self.saved_variables = {}
        self.machine = None
        self.record = None
        super().__init__(func)

    def __call__(self, *args, **kwargs):
        result = self._func(*args, *kwargs)
        # generate record
        general = {
            'function_name': self._func.__name__,
            'datetime': str(datetime.now()),
            'version': self.get_code_version(),
            'user': getuser(),
        }

        function_arguments = self.build_arg_dict(args, kwargs)
        self.record = [{'general': general,
                        'vcs': self.get_code_version(),
                        'function_arguments': function_arguments,
                        'saved_variables': self.saved_variables,
                        'result': str(result)}]

        # verify the machine
        if self.machine is None:
            try:
                self.machine = function_arguments['machine']
            except KeyError as e:
                msg = f"The key 'machine' is required to identify the correct database file and was not found in the " \
                      f"signature of the function '{self._func.__name__}'. Either add this as a function argument, " \
                      f"or initialise the logger with the correct machine e.g. '@FLPLogger(FacilityMachines.M3)'. "
                raise KeyError(msg) from e
        return result

    def log(self, key, value):
        self.saved_variables[key] = value

    @classmethod
    def with_machine(cls, machine: FacilityMachines):
        """Decorator factory allowing user to manually specify the machine
        without requiring it as an unused function argument"""

        def inner(func):
            flp_logger = cls(func)
            flp_logger.machine = machine
            return flp_logger

        return inner

    def recall_most_recent(self, func, *args, **kwargs):
        """Returns dictionary of the most recently called arguments for func.
        This is useful just for inspection but also full dictionary can be passed to """
        raise NotImplementedError

    def rerun_most_recent(self, func, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def get_code_version():
        """This facility uses a monorepo for all their """
        return "1.2.6"


if __name__ == '__main__':
    @FacilityLogger
    def my_processing_function(shot_number, machine, foo=False, bar=False):
        log(key='top_level_function', value='intermediate_value_1')
        double_shot_number = nested_function(shot_number)
        return double_shot_number

    def nested_function(a):
        log(key='nested_function', value='intermediate_value_1')
        return a * 2

    my_processing_function(21, FacilityMachines.M3, bar=True)
    print(my_processing_function.logger.record)

    @FacilityLogger.with_machine(FacilityMachines.M3)
    def my_processing_function_specifically_for_m3(shot_number, foo=False, bar=False):
        return shot_number

    my_processing_function_specifically_for_m3(42, foo=True)

    print(my_processing_function_specifically_for_m3.logger.record)
