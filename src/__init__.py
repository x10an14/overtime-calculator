"""Base module containing the global app variable++."""
from contextlib import ContextDecorator
from datetime import datetime
from datetime import timedelta
import logging

# PIP import:
from sanic import Sanic


app = Sanic("overtime-calculator")

default_parse_fmt = "%d-%m-%Y %H:%M:%S"
default_work_hours_in_week = timedelta(hours=40)
default_work_days = {"mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5}
logging_format = "%(process)d [%(asctime)s] \
%(levelname)s::%(module)s:%(lineno)d: "


def _get_current_time_string(just_time_string=False):
    if just_time_string:
        return datetime.now().strftime(default_parse_fmt)
    return datetime.now().strftime("[{}]: ".format(default_parse_fmt))


# Primarily useful for debugging of json objects
# which contain datetime.datetime objects.
# http://stackoverflow.com/a/22238613
#   More can be added over time...
def _serialize_json(obj, time_format=None):
    if isinstance(obj, datetime):
        serialized = obj.strftime(
            time_format if time_format is not None else default_parse_fmt)
        return serialized
    elif isinstance(obj, timedelta):
        serialized = str(obj)
        return serialized
    elif isinstance(obj, tuple):
        serialized = str(list(obj))
        return serialized
    elif isinstance(obj, set):
        serialized = list(obj)
        return serialized
    raise TypeError


def log_function_entry_and_exit(decorated_function):
    """Function decorator logging entry + exit (as logging.info), and parameters (as logging.debug) of functions."""
    from functools import wraps

    @wraps(decorated_function)
    def wrapper(*dec_fn_args, **dec_fn_kwargs):
        # Log function entry
        func_name = decorated_function.__name__
        log = logging.getLogger(func_name)
        log.info('Entering {}()...'.format(func_name))

        # get function params (args and kwargs)
        arg_names = decorated_function.__code__.co_varnames
        params = dict(
            args=dict(zip(arg_names, dec_fn_args)),
            kwargs=dec_fn_kwargs)

        log.debug(
            "\t" +
            ', '.join([
                '{}={}'.format(str(k), repr(v)) for k, v in params.items()]))
        # Execute wrapped (decorated) function:
        out = decorated_function(*dec_fn_args, **dec_fn_kwargs)
        log.info('Done running {}()!'.format(func_name))

        return out
    return wrapper


class TrackEntryAndExit(ContextDecorator):
    """
    A context manager and function decorator in-one for logging(!).

    See https://docs.python.org/3/library/contextlib.html#using-a-context-manager-as-a-function-decorator
    """

    def __init__(self, name):
        """Why is this doc-string required?..."""
        self.name = name

    def __enter__(self):
        """Why is this doc-string required?..."""
        logging.info(_get_current_time_string() + 'Entering: {}'.format(self.name))

    def __exit__(self, exc_type, exc, exc_tb):
        """Why is this doc-string required?..."""
        logging.info(_get_current_time_string() + 'Exiting: {}'.format(self.name))
