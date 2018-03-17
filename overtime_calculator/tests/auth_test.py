import os
import shutil
import pytest
import unittest
import tempfile

import hug
from hypothesis import given
from hypothesis import strategies as st
from usernames import is_safe_username

from overtime_calculator.src import api
from overtime_calculator.src.auth import get_user_folder


VALID_PASSWORD = st.text(min_size=6)
VALID_USERNAME = st.from_regex(r'[a-zA-Z]+[a-zA-Z0-9_-]*[a-zA-Z0-9]+')


@given(
    user=VALID_USERNAME,
    pw=VALID_PASSWORD,
)
def test_a_registration(user: str, pw: str):
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
        assert response.data == dict(error='Illegal character/word in username, try another one.')

# @given(
#     user=VALID_USERNAME,
#     pw=VALID_PASSWORD,
# )
# def test_b_user_sign_in(user: str, pw: str):
#     if not test_a_registration(user=user, pw=pw) == dict(status='Ok'):
#         return
#     response = hug.test.post(
#         api,
#         '/register',
#         dict(username=user, password=pw),
#     )
#     if is_safe_username(user):
#         # IMPORTANT:
#         # Do not create folder until username is deemed safe
#         user_folder = get_user_folder(user)
#         if user_folder.exists():
#             assert response.data == dict(error='Username already in use.')
#         else:
#             assert response.data == dict(status='Ok')
#     else:
#         assert response.data == dict(error='Illegal character/word in username, try another one.')

# class TestUserSignIn(unittest.TestCase):
#     @given(
#         user=VALID_USERNAME,
#         pw=VALID_PASSWORD,
#     )
#     def test_registration(user: str, pw: str):
#         response = hug.test.post(
#             api,
#             '/register',
#             dict(username=user, password=pw),
#         )
#         assert response.data == dict(status='ok')

# @given(
#     user=VALID_USERNAME,
#     pw=VALID_PASSWORD,
# )
# def test_signin(user: str, pw: str):
#     # First ensure sign-in:
#     test_registration(user=user, pw=pw)
#     response = hug.test.post(
#         api,
#         '/signin',
#         dict(username=user, password=pw),
#     )
#     assert response.data['token'] is not None

#     def teardown_module(self):
#         user_folder = get_user_folder('test1')
#         shutil.rmtree(str(user_folder), ignore_errors=False)

