""" Utility functions """
import functools
import traceback

def catch_exception(f):
    """ Decorator that logs a traceback from the class in question """
    @functools.wraps(f)
    def func(*args, **kwargs): # pylint: disable=inconsistent-return-statements
        try:
            return f(*args, **kwargs)
        except: # pylint: disable=bare-except
            args[0].log(traceback.format_exc())
    return func
