from functools import wraps
import logging

import jwt

default_parse_fmt = "%d-%m-%Y %H:%M:%S"


def get_secret():
    return 'sflkjsdjkfd'


def token_verify(token):
    secret = get_secret()
    try:
        return jwt.decode(token, secret, algorithm='HS256')
    except jwt.DecodeError:
        return False


def log_function_entry_and_exit(decorated_function):
    '''
    Function decorator logging time spent.

    Logging entry + exit (as logging.info),
    and parameters (as logging.debug) of functions.
    '''

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
