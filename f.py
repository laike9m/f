import sys


# TODO: stderr?

class F:
    __name__ = 'F'

    def __call__(self, *args):
        """Check argument and return the correct decorator.

        If args[0] is a function, then we assume f is used without argument:

            @f
            def function():
                ...

        If args[0] is not a function, we assume f is called with one or two
        arguments:

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

        if not args:
            raise TypeError(('f should be used as decorator, '
                             'not called directly'))
        elif callable(args[0]):
            function = args[0]

            @functools.wraps(function)
            def decorator(*args, **kwargs):
                with open('temp.log', 'w') as log_file:
                    sys.stdout = log_file
                    result = function(*args, **kwargs)
                    sys.stdout = sys.__stdout__
                    return result

            return decorator
        else:
            if len(args) == 1:
                filename = args[0]
                mode = 'w'
            elif len(args) == 2:
                filename, mode = args
            else:
                raise TypeError('f accepts one or two arguments.')

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
