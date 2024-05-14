import os
from datetime import datetime, timedelta

# in minutes
TOKEN_EXPIRY = 30
TOKEN_CACHE_FILE = "token.txt"


def cache_token(token):
    with open(TOKEN_CACHE_FILE, "w") as file:
        file.write(token)


def file_modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.fromtimestamp(t)


def read_token():
    if not os.path.exists("token.txt"):
        return

    with open(TOKEN_CACHE_FILE, "r") as file:
        token = file.read()

    return token


def is_valid_token(token):

    if not token:
        return False

    last_modified = file_modification_date(TOKEN_CACHE_FILE)
    expiry_time = timedelta(minutes=TOKEN_EXPIRY) + last_modified
    time_now = datetime.now()
    if expiry_time < time_now:
        return False

    return True


def rest_token_cache():
    with open(TOKEN_CACHE_FILE, "w") as file:
        file.write("")
