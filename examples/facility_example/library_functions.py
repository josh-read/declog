from examples.facility_example.logger import FacilityLogger, FacilityMachines


@FacilityLogger
def my_processing_function_for_any_machine(machine: FacilityMachines, shot_number: int):
    return machine.value * shot_number


@FacilityLogger.set(machine=FacilityMachines.M3)
def my_processing_function_for_m3(shot_number: int):
    return shot_number
