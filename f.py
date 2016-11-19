import sys

__author__ = 'laike9m <laike9m@gmail.com>'


DEFAULT_FILE = 'tmp.log'
DEFAULT_MODE = 'w'


class F:
    __name__ = 'F'
    _sys = __import__('sys')
    _functools = __import__('functools')
    DEFAULT_FILE = DEFAULT_FILE
    DEFAULT_MODE = DEFAULT_MODE

    # TODO: to stdout
    def __enter__(self, filename=DEFAULT_FILE, mode=DEFAULT_MODE,
                  stdout=False):
        self._sys.stdout = open(filename, mode)

    def __exit__(self, exception_type, exception_value, traceback):
        self._sys.stdout.close()
        self._sys.stdout = self._sys.__stdout__

    def __call__(self, filename=DEFAULT_FILE, mode=DEFAULT_MODE, stdout=False):
        """Check argument and return the correct decorator.

        If the first argument is a function, then we assume f is called without
        argument:

            @f
            def function():
                ...

        If the first argument is not a function, we assume f is called with one
        or two arguments:

            @f('really_import.log')
            def function():
                ...

            @f('really_import.log', 'a')
            def function():
                ...
        """
        # Prior to 3.4, when module is destroyed, __dict__ values are set to
        # None, so import here. See http://stackoverflow.com/questions/25649676
        if callable(filename):
            function = filename

            @self._functools.wraps(function)
            def decorator(*args, **kwargs):
                with open(self.DEFAULT_FILE, self.DEFAULT_MODE) as log_file:
                    self._sys.stdout = log_file
                    result = function(*args, **kwargs)
                    self._sys.stdout = self._sys.__stdout__
                    return result

            return decorator
        else:
            def decorator(function):
                @self._functools.wraps(function)
                def wrapper(*args, **kwargs):
                    with open(filename, mode) as log_file:
                        self._sys.stdout = log_file
                        result = function(*args, **kwargs)
                        self._sys.stdout = self._sys.__stdout__
                        return result

                return wrapper
        return decorator


sys.modules['f'] = F()
