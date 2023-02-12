## The problem

- Existing logging libraries are geared towards logging for
  long-running services
- Sometimes we write code to execute a routine, more like a
  script. This library aims to be a convenient logger for these
  functions with minimal boilerplate.
- We often repeat the same analysis routine for many datasets.
- Often we require not only the final output of the routine, but wish to
  log intermediate values.
- If we compare two results, we need to know whether the analysis
  code was the same or different. (Most obvious way to do this is
  to compare code version, however it is not always this simple.)
- Logging should be easy and not require the user to have to figure
  out correct paths to store results.

## The solution

- Decorate the 'main' function which is the top level entry point to the
  analysis routine.
- All settings should be managed in the arguments
  supplied to the function, which allows them to be captured by the decorator.
- Logging is still achieved simply with the `log` function, which will ascend
  the call stack until it reaches the `__call__` method of the `Logger` at
  which point the `Logger` will handle the logged variable.