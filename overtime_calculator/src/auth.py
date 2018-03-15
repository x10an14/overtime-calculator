import hug
import bcrypt
import jwt
import os

def get_users_folder(username):
    return "Users/" + username

def get_secret():
    return 'sflkjsdjkfd'

def token_verify(token):
    secret = get_secret()
    try:
        return jwt.decode(token, secret, algorithm='HS256') 
    except jwt.DecodeError:
        return False

# This is used in protected api paths. Ex: hug.get('/protected', requires=auth.token_key_authentication)
token_key_authentication = hug.authentication.token(token_verify)

@hug.post('/register')
def register_user(username, password):
    if os.path.exists(get_users_folder(username)):
        return {'error' : 'username already in use'}
    try:
        os.makedirs(get_users_folder(username))
        hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt()) # 12 is default salt rounds
        with open(get_users_folder(username) + '/password.txt', 'wb') as f:
            f.write(hashed_password)
        return {'status' : 'ok'}
    except:
        return {'error' : 'something went wrong with user registration'}

@hug.post('/signin')
def signin_user(username, password):
    secret = get_secret()
    if os.path.exists(get_users_folder(username)):
        try:
            with open(get_users_folder(username) + '/password.txt', 'rb') as f:
                hashed_password = f.readline()
            if bcrypt.checkpw(str.encode(password), hashed_password):
                return {"token" : jwt.encode({'user': username}, secret, algorithm='HS256')}
        except:
            return {'error' : 'something went wrong with user signin'}
    return {'error': 'Invalid credentials'}