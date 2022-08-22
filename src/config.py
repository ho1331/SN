from datetime import timedelta
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    # jwt
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # SQLAlchemy
    DB_HOST = getenv('POSTGRES_HOST')
    DB_USER = getenv('POSTGRES_USER')
    DB_PASSWORD = getenv('POSTGRES_PASSWORD')
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/postgres'
    )
