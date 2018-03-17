import hug
import bcrypt
from hypothesis import given
from hypothesis import strategies as st
from usernames import is_safe_username

from overtime_calculator.src import api
from overtime_calculator.src.auth import get_user_folder


VALID_PASSWORD = st.text(min_size=6)
VALID_USERNAME = st.from_regex(r'[a-zA-Z]+[a-zA-Z0-9_-]*[a-zA-Z0-9]+')


def _sign_in_user(user: str, pw: str):
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


@given(
    user=VALID_USERNAME,
    pw=VALID_PASSWORD,
)
def test_a_registration(user: str, pw: str):
    _sign_in_user(user, pw)


@given(
    user=VALID_USERNAME,
    pw=VALID_PASSWORD,
)
def test_signin(user: str, pw: str):
    # First ensure sign-in:
    _sign_in_user(user, pw)

    if is_safe_username(user):
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
