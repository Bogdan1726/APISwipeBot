import os
from dotenv import load_dotenv
from pathlib import Path
from pymongo import MongoClient
from aioredis import Redis


load_dotenv()

redis = Redis()


TOKEN = str(os.getenv('TOKEN'))
HOST = str(os.getenv('HOST'))

# region db
DB_HOST = str(os.getenv('DB_HOST'))
DB_PORT = int(os.getenv('DB_PORT'))
DB_NAME = str(os.getenv('DB_NAME'))
# endregion db

# region language
I18N_DOMAIN = 'APISwipeBot'
LOCALES_DIR = 'locales'
# endregion language

DEFAULT_IMAGE = "https://st4.depositphotos.com/14953852/22772/v/600/depositphotos_227725052-stock-illustration-no-image-available-icon-flat.jpg"
