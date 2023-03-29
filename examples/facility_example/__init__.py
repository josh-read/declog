from pprint import pprint

from examples.facility_example.library_functions import (
    my_processing_function_for_any_machine,
    my_processing_function_for_m3,
)
from examples.facility_example.logger import FacilityDatabase, FacilityLogger
from examples.facility_example.machines import FacilityMachines


if __name__ == "__main__":
    # set up the directory structure
    for path in FacilityDatabase.gen_db_paths().values():
        path.parent.mkdir(parents=True, exist_ok=True)

    my_processing_function_for_any_machine(FacilityMachines.M2, 21)
    my_processing_function_for_m3(42)
    pprint(FacilityLogger.db)
