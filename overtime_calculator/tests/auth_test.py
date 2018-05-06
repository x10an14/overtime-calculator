from collections import namedtuple

import hug
import bcrypt
from hypothesis import given
from hypothesis.strategies import data, composite
from hypothesis import strategies as st
from usernames import is_safe_username
from usernames.validators import username_regex as _valid_username_regex

from overtime_calculator.src import api
from overtime_calculator.src.auth import get_user_folder

# For use by hypothesis
User = namedtuple('User', ['handle', 'password'])
# Ref:
# https://github.com/theskumar/python-usernames/blob/master/usernames/validators.py#L9
VALID_USERNAME = st.from_regex(_valid_username_regex)
VALID_PASSWORD = st.text(min_size=6)

# List of existing users created
_EXISTING_USERS = set()


# @composite
def new_user(draw, username=VALID_USERNAME, password=VALID_PASSWORD):
    new_user = User(handle=username, password=password)
    _EXISTING_USERS.append(new_user)
    return new_user


def _register_user(user: str, pw: str):
    response = hug.test.post(
        api,
        '/register',
        dict(username=user, password=pw),
    )
    if is_safe_username(user):
        # IMPORTANT:
        # Do not create folder until username is deemed safe
        user_folder = get_user_folder(user)
        if user_folder.exists():
            assert response.data == dict(error='Username already in use.')
        else:
            assert response.data == dict(status='Ok')
    else:
        assert response.data == dict(
            error='Illegal character/word in username, try another one.'
        )

    # Return so calling function can know result...
    return response.data


@given(
    user=VALID_USERNAME,
    pw=VALID_PASSWORD,
)
def test_signin(user: str, pw: str):
    # First ensure sign-in:
    register_response = _register_user(user, pw)
    if not register_response == dict(status='Ok'):
        # Uninteresting username
        return

    if is_safe_username(user):
        response = hug.test.post(
            api,
            '/signin',
            dict(username=user, password=pw),
        )
        user_pw_file = get_user_folder(user) / 'password.txt'
        if not bcrypt.checkpw(
            str.encode(pw),
            user_pw_file.open(mode='rb').readline()
        ):
            response.data = dict(error='Invalid credentials.')
            return

        # If password checks out:
        assert response.data['token'] and response.data['token'] is type(str)
