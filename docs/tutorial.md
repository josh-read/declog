# Tutorial

This tutorial is written to demonstrate some useful functionality
built into the DecLog library, as well as how to write your own Database
backend and extend the BaseLogger.

Say for example, that we want to overhaul the way we record analysis
results at a research lab.

Our research lab has an extensive analysis library, providing well tested
and documented functions and classes for performing common analysis
routines on our experimental data. Each experiment involves firing a 'shot'
on one of the machines, and a number of measurements are made depending on
the interaction between the machine and the load.

Let's create an object representing the various options for a machine containing
all the possible machines. Using an Enum, we can store the different machine names
with the corresponding folder number:

```python
--8<-- "examples/facility_example/machines.py"
```

## Setting custom unique keys

The most basic customisation one can make to the BaseLogger
is to add custom keys. In fact, all the DefaultLogger does is
inherit from the BaseLogger, set the database to the PickleDatabase
and set the database keys to the function name and datetime.

At our research lab, every experiment is conducted on one of several
machines and is assigned a shot number. So for example, two separate
experiments could be conducted on Machine A and Machine B but they
could share the same shot number.

Clearly, we need to differentiate between these experiments, so we need
to set the keys to make this clear:

```python
from declog.logger import BaseLogger
from declog.database import BaseDatabase

class FacilityLogger(BaseLogger):
    db = BaseDatabase()
    unique_keys = "machine shot_number function_name datetime".split()
```

Now, when the FacilityLogger is applied to a function, every time the function
is run a new entry
will be created in the underlying database, using the captured values
in the order
specified in `unique_keys`.

## Manually setting key values

The intention of this library is to reduce work for developers by automatically logging all the arguments supplied to an
analysis function. However, due to the key system, it is required to supply some variables for logging, even if they are
not actually required by the function. One option is to make the key a redundant argument to the function, this is
inconsistent with PEP8 and will not pass flake8 checks. Instead, one can use the `set()` class method from the
BaseLogger.

```python
--8<-- "examples/facility_example/library_functions.py"
```

## Using a custom database

So far, our Logger uses the BaseDatabase, which is an abstract type that
defines how a database is stored in memory, but doesn't specify any
persistent file format. There are a couple of built-in options, but this
example will demonstrate how to create your own.

This research lab already has its own data storage protocol, each machine
has a json file which is used to log shot variables for that machine. See
below for this illustrated as a tree diagram.

```
.
└── data/
    ├── 02_M2/
    │   ├── metadata/
    │   │   └── shot_db.json
    │   ├── raw_data/
    │   │   ├── s0001
    │   │   ├── s0002
    │   │   └── ...
    │   └── processed_data/
    │       ├── s0001
    │       ├── s0002
    │       └── ...
    └── 03_M3/
        └── ...
```

In order to go between the database interface used by the logger and our own
custom storage format, we need to create a custom database:

```python
--8<-- "examples/facility_example/logger.py:FacilityDatabase"
```

Finally, we need to supply this as the database to our logger:

```python
from declog.logger import BaseLogger
from examples.facility_example.logger import FacilityDatabase

class FacilityLogger(BaseLogger):
    db = FacilityDatabase()
    unique_keys = "machine shot_number function_name datetime".split()
```

## Capturing information about the environment

So far, we have seen that we are able to log values using
the `log` function and that the function arguments are captured
automatically by the Logger. But what if we want to automatically
capture information about the environment the function is being called
in?

Let's go back to our example research facility. We would like to know what
version of the code we are running at the time. Given the examples so far,
we have the options of making a `log` call in every function, or making it
an argument to all functions, neither of which are particularly
maintainable.

DecLog gives us the option of using `logged_properties`.

```python
from declog import logged_property
from declog.logger import DefaultLogger

class MyLogger(DefaultLogger):

    @logged_property
    def meaning_of_life(self):
        return 42

    
assert MyLogger(lambda: None).meaning_of_life == 42

```

These behave just like normal properties, and can be accessed from an
instance at any time. Whenever a decorated function is called, any logged
properties are added to the database entry, and can be used as keys if
desired.

Logged properties are also how the DefaultLogger captures the name of the
function and time of the function call. If we look at the class definition,
we find that it inherits the `FunctionNameMixin` and `DateTimeMixin`, each
of which define one `logged_property` method. In `declog.logger.mixins`
a few commonly used `logged_property`s are defined. It is worth taking
a look at these mixins, as they may be useful in your logger.