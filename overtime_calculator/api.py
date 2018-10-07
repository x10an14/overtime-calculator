import hug

from overtime_calculator import auth


def _hello_user(user_name: str):
    return f"Hello, {user_name}!"


@hug.extend_api()
def auth_api():
    return [auth]


@hug.get('/hello', requires=auth.token_key_authentication)
def hello_world_signed_in(user: hug.directives.user):
    return _hello_user(user['user'])
