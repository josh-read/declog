import inspect
from typing import Any


def _get_var_name(val: Any, n: int = 1) -> str:
    """Get the variable name assigned to `val`.

    Step back through the frames in the call stack,
    then check that frame for the `val` and return
    the name of the variable it is assigned to."""
    # step back to frame of interest
    frame = inspect.currentframe()
    for _ in range(n):
        frame = frame.f_back
    # search through frame's local variables
    for var_name, var_val in frame.f_locals.items():
        if var_val is val:
            return var_name
    raise KeyError(f"The val {val} was not found in frame {frame}.")
