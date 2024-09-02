from dotenv import load_dotenv
import os
import hashlib

load_dotenv()

BASE_URL = 'http://app.redforester.com/api'

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HASHED_PASSWORD = hashlib.md5(PASSWORD.encode()).hexdigest()

AUTH = (USER, HASHED_PASSWORD)

TYPE_CATEGORY = 'ff69b91f-381c-41fa-9c1a-7aaaed7a365d'
TYPE_NONTYPE = None
