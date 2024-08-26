from dotenv import load_dotenv
import os
import hashlib

load_dotenv()

BASE_URL = 'http://app.redforester.com/api/'
AUTH_URL = BASE_URL + 'user'

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')


def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


AUTH = (USER, md5(PASSWORD))
HEADERS = {'Content-Type': "application/json"}
