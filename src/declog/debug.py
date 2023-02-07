from declog.logger import Logger, log


class StdOutLogger(Logger):

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
