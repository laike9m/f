import sys

__author__ = 'laike9m <laike9m@gmail.com>'


DEFAULT_FILE = 'tmp.log'
DEFAULT_MODE = 'w'


class F(object):
    # Prior to 3.4, when module is destroyed, __dict__ values are set to
    # None, so import here. See http://stackoverflow.com/questions/25649676
    __name__ = 'F'
    _sys = __import__('sys')
    _functools = __import__('functools')
    DEFAULT_FILE = DEFAULT_FILE
    DEFAULT_MODE = DEFAULT_MODE

    # TODO: to stdout
    def __enter__(self):
        self._sys.stdout = open(self.DEFAULT_FILE, self.DEFAULT_MODE)

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
            # record outer instance to be used inside below class
            F_inst = self

            class DeccoratorWithContextManager(object):
                """
                This class is both a class decorator and a context manager.
                """
                def __call__(self, function):
                    @F_inst._functools.wraps(function)
                    def wrapper(*args, **kwargs):
                        with open(filename, mode) as log_file:
                            F_inst._sys.stdout = log_file
                            result = function(*args, **kwargs)
                            F_inst._sys.stdout = F_inst._sys.__stdout__
                            return result
                    return wrapper

                def __enter__(self):
                    F_inst._sys.stdout = open(filename, mode)

                def __exit__(self, exception_type, exception_value, traceback):
                    F_inst._sys.stdout.close()
                    F_inst._sys.stdout = F_inst._sys.__stdout__

            return DeccoratorWithContextManager()


sys.modules['f'] = F()
