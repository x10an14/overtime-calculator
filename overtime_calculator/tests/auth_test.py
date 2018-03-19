import re
from pathlib import Path
from collections import namedtuple

import hug
import bcrypt
from hypothesis import data
from hypothesis import given
from hypothesis import assume
from hypothesis import composite
from hypothesis import strategies as st
from usernames import is_safe_username

from . import existing_usernames
from overtime_calculator.src import api
from overtime_calculator.src.auth import get_user_folder

# For use by hypothesis
User = namedtuple('User', ['handle', 'password'])
# Ref:
# https://github.com/theskumar/python-usernames/blob/master/usernames/validators.py#L9
from usernames.validators import username_regex as _valid_username_regex
VALID_USERNAME = st.from_regex(_valid_username_regex)
VALID_PASSWORD = st.text(min_size=6)

# List of existing users created
_EXISTING_USERS = set()

@composite
def new_user(draw, username=VALID_USERNAME, password=VALID_PASSWORD):
    new_user =  User(handle=username, password=password)
    _EXISTING_USERS.append(new_user)
    return new_user



def _register_user(user: str, pw: str):
    response = hug.test.post(
        api,
        '/register',
        dict(username=user, password=pw),
    )
    if not is_safe_username(user):
        assert response.data == dict(error='Illegal character/word in username, try another one.')
        return response.data

    # IMPORTANT:
    # Do not create folder until username is deemed safe
    user_folder = get_user_folder(user)
    if user_folder.exists():
        assert response.data == dict(error='Username already in use.')
        return response.data

    assert response.data == dict(status='Ok')
    return response.data


@given(data())
def test_signin(data):
    user = data.draw(
        VALID_USERNAME | st.sampled_from(new_user())
    )
    if user not in existing_usernames:
        pw = data.draw(VALID_PASSWORD)
        register_response = _register_user(user, pw)
    else:


    # First ensure sign-in:
    register_response = _register_user(user, pw)
    assume(register_response == dict(status='Ok'))

    response = hug.test.post(
        api,
        '/signin',
        dict(username=user, password=pw),
    )
    user_pw_file = get_user_folder(user) / 'password.txt'
    if not bcrypt.checkpw(str.encode(pw), user_pw_file.open(mode='rb').readline()):
        response.data = dict(error='Invalid credentials.')
        return

    # If password checks out:
    assert response.data['token'] and response.data['token'] is type(str)
