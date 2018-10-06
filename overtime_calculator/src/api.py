import hug

from . import token_verify
from overtime_calculator.src import auth


# This is used in protected api paths. Ex: hug.get('/protected', requires=auth.token_key_authentication)
token_key_authentication = hug.authentication.token(token_verify)

def _hello_user(user_name: str):
    return f"Hello, {user_name}!"

@hug.extend_api()
def auth_api():
    return [auth]


@hug.get('/hello', requires=token_key_authentication)
def hello_world_signed_in(user: hug.directives.user):
    return _hello_user(user['user'])
