import shutil

import hug
from falcon import HTTP_200, HTTP_409, HTTP_401, HTTP_201

from overtime_calculator import api
from overtime_calculator.auth import get_user_folder

EXISTING_USER = 'test1'
UNREGISTERED_USER = 'test2'


def test_registration_of_new_user_and_sign_in():
    response = hug.test.post(
        api,
        '/register',
        {'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    assert(response.status == HTTP_201)
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert response.data == {'status': 'ok'}


def test_second_registration_of_registered_user():
    response = hug.test.post(
        api_or_module=api,
        url='/register',
        body={'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    print(response.status)    # Will only show if test fails and is run with --verbose (-v)
    assert(response.status == HTTP_409)
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert response.data == dict(error='username already in use')


def test_sign_in_of_existing_user():
    response = hug.test.post(
        api_or_module=api,
        url='/signin',
        body={'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    print(dir(response))    # Will only show if test fails and is run with --verbose (-v)
    print(response.status)    # Will only show if test fails and is run with --verbose (-v)
    assert(response.status == HTTP_200)
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert 'token' in response.data and response.data['token']


def test_sign_in_of_non_existing_user():
    response = hug.test.post(
        api,
        '/signin',
        {'username': UNREGISTERED_USER, 'password': EXISTING_USER}
    )
    print(response.status)    # Will only show if test fails and is run with --verbose (-v)
    assert(response.status == HTTP_401)
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert response.data == dict(error='Invalid credentials')


def test_sign_in_of_wrong_pw():
    response = hug.test.post(
        api,
        '/signin',
        {'username': EXISTING_USER, 'password': 'yoyo'}
    )
    print(response.status)    # Will only show if test fails and is run with --verbose (-v)
    assert(response.status == HTTP_401)
    print(response.data)    # Will only show if test fails and is run with --verbose (-v)
    assert response.data == dict(error='Invalid credentials')


def teardown_module():
    user_folder = get_user_folder(EXISTING_USER)
    shutil.rmtree(str(user_folder), ignore_errors=False)
