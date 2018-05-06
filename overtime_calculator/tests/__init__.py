from pathlib import Path


def existing_usernames():
    return [
        str(username)
        for username in
        (Path('data') / 'users').iterdir()
    ]
