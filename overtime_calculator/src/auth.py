import hug
import bcrypt
import jwt
import os
from pathlib import Path
from typing import Dict

from . import get_secret
from . import token_verify


# This is used in protected api paths. Ex: hug.get('/protected', requires=auth.token_key_authentication)
token_key_authentication = hug.authentication.token(token_verify)


def get_user_folder(username: str) -> Path:
    user_folder = Path('.') / 'data' / 'users' / username
    if not user_folder.exists():
        user_folder.mkdir(parents=True)
    return user_folder


@hug.post('/register')
def register_user(username, password):
    user_folder = get_user_folder(username)
    if user_folder.exists():
        return {'error' : 'username already in use'}
    try:
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) # 12 is default salt rounds
        user_pw_file = user_folder / 'password.txt'
        with user_pw_file.open(mode='w') as f:
            f.write(hashed_password)
        return {'status' : 'ok'}
    except:
        return {'error' : 'something went wrong with user registration'}


@hug.post('/signin')
def signin_user(username: str, password: str) -> Dict[str, str]:
    secret = get_secret()
    user_folder = get_user_folder(username)
    if user_folder.exists():
        try:
            user_pw_file = user_folder / 'password.txt'
            with user_pw_file.open() as f:
                hashed_password = f.readline()
            if bcrypt.checkpw(str.encode(password), hashed_password):
                return {"token" : jwt.encode({'user': username}, secret, algorithm='HS256')}
        except:
            return {'error' : 'something went wrong with user signin'}
    return {'error': 'Invalid credentials'}
