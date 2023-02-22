import inspect


def _get_var_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    (var_name,) = [name for name, val in callers_local_vars if val is var]
    return var_name
