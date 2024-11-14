from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

PATH_TO_DB = str(BASE_DIR / 'database' / 'source' / 'movies.db')
PATH_TO_MOVIES_CSV_FILE = str(BASE_DIR / 'files' / 'movies.csv')
