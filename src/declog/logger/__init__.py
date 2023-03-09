"""Loggers are classes which are applied to functions as decorators.
When the function is called, the `__call__` method of the Logger is
executed, which allows it to log the arguments supplied to the function,
in addition to other marked properties.

The Logger is separated from the database backends, allowing one logger to
be used with multiple backends and vice versa."""
