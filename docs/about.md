# About

[//]: # (what)
DecLog provides a framework for building unintrusive loggers for functions.
The `Logger` is applied to functions or methods as a decorator, and
automatically captures the arguments and return values, plus some optional
information about the environment. The user can also manually log values
with the `log` function. The `Logger` sends these values to a `Database`
which can be used interchangeably with different output formats. The
`Database` behaves similarly to a python dictionary, making it intuitive
to access past entries.

[//]: # (why)
DecLog was originally designed to integrate with a data analysis library
at a research facility in order to create an archive of results[^1]. Existing
logging libraries are geared towards long-running services by
producing a flat feed of messages (differentiable only by level i.e. info/
warning/error). DecLog is aimed at recording function calls, and stores
logged values in a hierarchical structure, using key-value pairs.

DecLog is available right now! Check out the [installation guide](install.md).

[^1]:
  The motivation for archiving results with function arguments and
  intermediate values, in addition to the code version, is that
  it makes the result entirely reproducible - a cornerstone of the scientific
  method.