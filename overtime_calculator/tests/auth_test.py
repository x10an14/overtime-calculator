import shutil
import pytest

import hug

from overtime_calculator.src import api
from overtime_calculator.src.auth import get_user_folder

EXISTING_USER = 'test1'
UNREGISTERED_USER = 'test2'


def test_registration_of_new_user():
    response = hug.test.post(
        api,
        '/register',
        {'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert response.data == {'status': 'ok'}


def test_second_registration_of_registered_user():
    response = hug.test.post(
        api,
        '/register',
        {'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert response.data == dict(error='username already in use')


def test_sign_in_of_existing_user():
    response = hug.test.post(
        api,
        '/signin',
        {'username': EXISTING_USER, 'password': EXISTING_USER}
    )
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert 'token' in response.data and response.data['token']


def teardown_module():
    user_folder = get_user_folder(EXISTING_USER)
    shutil.rmtree(str(user_folder), ignore_errors=False)

