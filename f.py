import sys

__author__ = 'laike9m <laike9m@gmail.com>'


DEFAULT_FILE = 'tmp.log'
DEFAULT_MODE = 'w'


class F:
    __name__ = 'F'
    DEFAULT_FILE = DEFAULT_FILE
    DEFAULT_MODE = DEFAULT_MODE

    def __call__(self, filename=DEFAULT_FILE, mode=DEFAULT_MODE):
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
        import functools
        import sys

        if callable(filename):
            function = filename

            @functools.wraps(function)
            def decorator(*args, **kwargs):
                with open(self.DEFAULT_FILE, self.DEFAULT_MODE) as log_file:
                    sys.stdout = log_file
                    result = function(*args, **kwargs)
                    sys.stdout = sys.__stdout__
                    return result

            return decorator
        else:
            def decorator(function):
                @functools.wraps(function)
                def wrapper(*args, **kwargs):
                    with open(filename, mode) as log_file:
                        sys.stdout = log_file
                        result = function(*args, **kwargs)
                        sys.stdout = sys.__stdout__
                        return result

                return wrapper
        return decorator


sys.modules['f'] = F()
