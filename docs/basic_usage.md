# Basic Usage

Analysis code is typically run through a main processing function, 
which draws together library code to produce a meaningful result.

The logger is applied as a decorator to the processing function,
and captures the function arguments, intermediate values marked
with `log` and the return value.

```python
from declog.loggers.logger import Logger, log
from declog.database.database import Database


class MyLogger(Logger):
    db = Database()
    unique_keys = ['function_name', 'datetime']


@MyLogger
def my_processing_function(a, b, c=2, d=3.14):
    ab = a * b
    log('ab', ab)
    cd = c - d
    log(cd)
    return ab + cd


if __name__ == '__main__':
    my_processing_function(1, 5)
    print(my_processing_function.db)

```

The Logger is designed to be flexible, in the above example the base class
Database is used which only saves logged items to a dictionary in memory.
For use as a proper logger, the database must be saved to memory. View the
[reference](reference.md) for options or create your own backend as in the
[tutorial](tutorial.md).

For more information on usage, check out the [about](about.md) page or
[tutorials](tutorial.md) in the docs.