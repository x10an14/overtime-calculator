import hug
from overtime_calculator.src import auth

@hug.extend_api()
def auth_api():
    return [auth]
    