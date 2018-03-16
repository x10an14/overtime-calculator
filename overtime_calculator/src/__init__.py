from contextlib import ContextDecorator
from datetime import datetime
from datetime import timedelta
import logging


default_parse_fmt = "%d-%m-%Y %H:%M:%S"


def get_secret():
    return 'sflkjsdjkfd'


def log_function_entry_and_exit(decorated_function):
    '''
    Function decorator logging time spent.

    Logging entry + exit (as logging.info),
    and parameters (as logging.debug) of functions.
    '''
    from functools import wraps

    @wraps(decorated_function)
    def wrapper(*dec_fn_args, **dec_fn_kwargs):
        # Log function entry
        func_name = decorated_function.__name__
        logging.info(f"Entering {func_name}()...")

        # get function params (args and kwargs)
        arg_names = decorated_function.__code__.co_varnames
        params = dict(
            args=dict(zip(arg_names, dec_fn_args)),
            kwargs=dec_fn_kwargs
        )
        logging.debug(
            "\t" + ', '.join(
                [f"{k}={v}" for k, v in params.items()]
            )
        )
        # Execute wrapped (decorated) function:
        out = decorated_function(*dec_fn_args, **dec_fn_kwargs)
        logging.info(f"Done running {func_name}()!")

        return out
    return wrapper


class TrackEntryAndExit(ContextDecorator):
    '''
    A context manager and function decorator in-one for logging(!).

    See https://docs.python.org/3/library/contextlib.html#using-a-context-manager-as-a-function-decorator
    '''

    def __init__(self, name):
        '''Why is this doc-string required?...'''
        self.name = name

    def __enter__(self):
        '''Why is this doc-string required?...'''
        logging.info(_get_current_time_string() + f"Entering: {self.name}")

    def __exit__(self, exc_type, exc, exc_tb):
        '''Why is this doc-string required?...'''
        logging.info(_get_current_time_string() + f"Exiting: {self.name}")
