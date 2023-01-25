from declog.logger import Logger, log


class StdOutLogger(Logger):

    def __call__(self, *args, **kwargs):
        arg_dict = self.build_arg_dict(args, kwargs)
        print(arg_dict)
        result = self._func(*args, **kwargs)
        print(result)
        return result

    def log(self, key, value):
        print(f'{key}: {value}')


if __name__ == '__main__':

    @StdOutLogger
    def my_function(a, b, c=3, d=-2):
        ab = a * b
        log('ab', ab)
        cd = c / d
        log(cd)
        return ab + cd

    my_function(3, 7)
