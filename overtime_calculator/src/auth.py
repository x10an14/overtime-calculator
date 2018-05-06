from pathlib import Path
from typing import Dict

import hug
import jwt
import bcrypt
from usernames import is_safe_username

from . import get_secret
from . import token_verify


# This is used in protected api paths.
# Ex: hug.get('/protected', requires=auth.token_key_authentication)
token_key_authentication = hug.authentication.token(token_verify)


def get_user_folder(username: str) -> Path:
    user_folder = Path('.') / 'data' / 'users' / username
    if not user_folder.exists():
        user_folder.mkdir(parents=True)
    return user_folder


@hug.post('/register')
def register_user(
    username: str,
    password: str,
) -> Dict[str, str]:
    if not is_safe_username(username):
        return dict(
            error='Illegal character/word in username, try another one.'
        )

    user_folder = get_user_folder(username)
    if user_folder.exists():
        return {'error': 'Username already in use.'}

    hashed_password = bcrypt.hashpw(
        # 12 is default salt rounds
        str.encode(password), bcrypt.gensalt()
    )
    user_pw_file = user_folder / 'password.txt'
    with user_pw_file.open(mode='wb') as f:
        f.write(hashed_password)
    return {'status': 'Ok'}


@hug.post('/signin')
def signin_user(username: str, password: str):
    secret = get_secret()
    user_folder = get_user_folder(username)
    user_pw_file = user_folder / 'password.txt'
    if not user_pw_file.exists():
        return {'error': 'Invalid credentials.'}

    with user_pw_file.open(mode='rb') as f:
        hashed_password = f.readline()
    if not bcrypt.checkpw(str.encode(password), hashed_password):
        return {'error': 'Invalid credentials.'}

    # Password checked out:
    return {"token": jwt.encode({'user': username}, secret, algorithm='HS256')}
