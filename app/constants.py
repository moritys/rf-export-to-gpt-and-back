from dotenv import load_dotenv
import os
import sys
import hashlib

extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))

BASE_URL = 'https://app.redforester.com/api'

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HASHED_PASSWORD = hashlib.md5(PASSWORD.encode()).hexdigest()

AUTH = (USER, HASHED_PASSWORD)

TYPE_CATEGORY = 'ff69b91f-381c-41fa-9c1a-7aaaed7a365d'
TYPE_NONTYPE = None
