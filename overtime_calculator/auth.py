from pathlib import Path

import bcrypt
from falcon import HTTP_401, HTTP_409, HTTP_201
import hug
import jwt

from . import get_secret, token_verify


# This is used in protected api paths. Ex: hug.get('/protected', requires=auth.token_key_authentication)
token_key_authentication = hug.authentication.token(token_verify)


def get_user_folder(username: str) -> Path:
    user_folder = Path('.') / 'data' / 'users' / username
    if not user_folder.exists():
        user_folder.mkdir(parents=True)
    return user_folder


@hug.post('/register')
def register_user(username: str, password: str, response=None):
    user_folder = get_user_folder(username)
    user_pw_file = user_folder / 'password.txt'
    if user_pw_file.exists():
        response.status = HTTP_409
        return {'error': 'username already in use'}

    # 12 is default salt rounds
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    with user_pw_file.open(mode='wb') as f:
        f.write(hashed_password)
    response.status = HTTP_201
    return {'status': 'ok'}


@hug.post('/signin')
def signin_user(username: str, password: str, response=None):
    secret = get_secret()
    user_folder = get_user_folder(username)
    user_pw_file = user_folder / 'password.txt'
    if not user_pw_file.exists():
        response.status = HTTP_401
        return {'error': 'Invalid credentials'}

    with user_pw_file.open(mode='rb') as f:
        hashed_password = f.readline()
    if not bcrypt.checkpw(str.encode(password), hashed_password):
        response.status = HTTP_401
        return {'error': 'Invalid credentials'}
    return {
        "token": jwt.encode(
            {'user': username},
            secret,
            algorithm='HS256'
        )
    }
