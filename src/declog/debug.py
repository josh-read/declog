from declog.logger import Logger, log


class StdOutLogger(Logger):
    """
    Logger implementation which echos captured values to StdOut.

    Examples:
        The doctest below illustrates typical syntax and the types of values that can be captured, however the StdOutLogger
        cannot demonstrate

        >>> @StdOutLogger
        ... def my_function(a, b, c=3, d=-2):
        ...     ab = a * b
        ...     log('ab', ab)
        ...     cd = c / d
        ...     log(cd)
        ...     return ab + cd
        ...
        >>> my_function(3, 7, d=4)
        my_function(a=3, b=7, c=3, d=4)
        ab = 21
        cd = 0.75
        returns 21.75
    """

    def __call__(self, *args, **kwargs):
        self.print_signature(args, kwargs)
        result = self._func(*args, **kwargs)
        print(f"returns {result}")

    def log(self, key, value):
        print(f"{key} = {value}")

    def print_signature(self, args, kwargs):
        arg_dict = self.build_arg_dict(args, kwargs)
        arg_str = ", ".join(f"{k}={v}" for k, v in arg_dict.items())
        print(f"{self._func.__name__}({arg_str})")
