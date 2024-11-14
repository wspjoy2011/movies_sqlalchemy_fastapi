import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

PATH_TO_DB = str(BASE_DIR / 'database' / 'source' / 'movies.db')
PATH_TO_MOVIES_CSV_FILE = str(BASE_DIR / 'files' / 'movies.csv')

load_dotenv(BASE_DIR / '.env')

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_DB_PORT = os.environ['POSTGRES_DB_PORT']
POSTGRES_DB = os.environ['POSTGRES_DB']
