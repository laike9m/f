import sys

__author__ = 'laike9m <laike9m@gmail.com>'


DEFAULT_FILE = 'tmp.log'
DEFAULT_MODE = 'w'


class Logger(object):
    _sys = __import__('sys')

    def __init__(self, filename, mode):
        self.terminal = self._sys.__stdout__
        self.log = open(filename, mode)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def close(self):
        self.log.close()


class F(object):
    # Prior to 3.4, when module is destroyed, module's __dict__ values are set
    # to None, which affects imported modules like sys(which is in globals()),
    # so import them here.
    # See http://stackoverflow.com/questions/25649676
    __name__ = 'F'
    _sys = __import__('sys')
    _functools = __import__('functools')
    _Logger = Logger
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
            Logger = self._Logger

            class DecoratorWithContextManager(object):
                """
                This class is both a class decorator and a context manager.
                """
                def __call__(self, function):
                    @F_inst._functools.wraps(function)
                    def wrapper(*args, **kwargs):
                        F_inst._sys.stdout = Logger(filename, mode) \
                            if stdout else open(filename, mode)
                        result = function(*args, **kwargs)
                        F_inst._sys.stdout.close()
                        F_inst._sys.stdout = F_inst._sys.__stdout__
                        return result
                    return wrapper

                def __enter__(self):
                    F_inst._sys.stdout = Logger(filename, mode) \
                        if stdout else open(filename, mode)

                def __exit__(self, exception_type, exception_value, traceback):
                    F_inst._sys.stdout.close()
                    F_inst._sys.stdout = F_inst._sys.__stdout__

            return DecoratorWithContextManager()


sys.modules['f'] = F()
