import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str
    test_database_url: str
    show_count: int = 1000


dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

settings = Settings(
    _env_file=os.path.join(dir_path, '.env.example'),
    _env_file_encoding='utf-8',
)
