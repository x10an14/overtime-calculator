import shutil

import hug
from falcon import HTTP_201, HTTP_200, HTTP_401

from overtime_calculator import api
from overtime_calculator.auth import get_user_folder

EXISTING_USER = 'test1'


def setup_module():
    response = hug.test.post(
        api_or_module=api,
        url='/register',
        body={'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    assert(response.status == HTTP_201)


def test_hello_user():
    login = hug.test.post(
        api_or_module=api,
        url='/signin',
        body={'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    assert(login.status == HTTP_200)
    assert(login.data.get('token', None))

    auth_dict = dict(Authorization=login.data['token'])
    hello_user = hug.test.get(
        api_or_module=api,
        url='/hello',
        headers=auth_dict,
    )
    assert(hello_user.status == HTTP_200)
    assert(hello_user.data == api._hello_user(EXISTING_USER))


def test_hello_invalid_token():
    login = hug.test.post(
        api_or_module=api,
        url='/signin',
        body={'username': EXISTING_USER, 'password': EXISTING_USER},
    )
    assert(login.status == HTTP_200)
    assert(login.data.get('token', None))

    auth_dict = dict(Authorization='GARBAGE')
    hello_user = hug.test.get(
        api_or_module=api,
        url='/hello',
        headers=auth_dict,
    )
    assert(hello_user.status == HTTP_401)
    assert(hello_user.data != api._hello_user(EXISTING_USER))


def teardown_module():
    user_folder = get_user_folder(EXISTING_USER)
    shutil.rmtree(
        str(user_folder), ignore_errors=False)
