import shutil
import pytest

import hug

from overtime_calculator.src import api
from overtime_calculator.src.auth import get_user_folder


def test_register():
    user_name = 'test1'
    response = hug.test.post(
        api,
        '/register',
        {'username': user_name, 'password': user_name},
    )
    assert response.data == {'status': 'ok'}

def test_signin():
    response = hug.test.post(api, '/signin', {'username': 'test_1', 'password': 'test_1'})
    print(response.data)
    assert response.data['token'] is not None

def teardown_module():
    user_folder = get_user_folder('test1')
    shutil.rmtree(str(user_folder), ignore_errors=False)

