import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent

PATH_TO_MOVIES_CSV_FILE = str(BASE_DIR / 'database' / 'data_processing' / 'files' /'movies.csv')

MEDIA_DIR = BASE_DIR / 'media'
MEDIA_PROFILE_DIR = MEDIA_DIR / 'profile'


load_dotenv(BASE_DIR / '.env')

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_DB_PORT = os.environ['POSTGRES_DB_PORT']
POSTGRES_DB = os.environ['POSTGRES_DB']

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
