from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Path to folders and files
    BASE_DIR: Path = Path(__file__).parent.parent
    PATH_TO_MOVIES_CSV_FILE: str = str(BASE_DIR / 'database' / 'data_processing' / 'files' / 'movies.csv')
    MEDIA_DIR: Path = BASE_DIR / 'media'
    MEDIA_PROFILE_DIR: Path = MEDIA_DIR / 'profile'

    # Postgresql
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB_PORT: int
    POSTGRES_DB: str

    # Redis
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int

    # Email
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_HOST_USER: str
    EMAIL_HOST_PASSWORD: str

    # model_config = SettingsConfigDict(env_file=BASE_DIR.parent / '.env', extra='ignore', case_sensitive=True)
