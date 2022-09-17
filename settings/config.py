import os
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient

load_dotenv()

TOKEN = str(os.getenv('TOKEN'))
API = str(os.getenv('API'))

# region db
DB_HOST = str(os.getenv('DB_HOST'))
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = str(os.getenv('DB_NAME'))
# endregion db

# region language
I18N_DOMAIN = 'APISwipeBot'
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locale'
# endregion language
