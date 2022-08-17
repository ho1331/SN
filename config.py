from os import getenv


class Config:
    """Set Flask config variables."""
    # SQLAlchemy
    DB_HOST = getenv("POSTGRES_HOST")
    DB_USER = getenv("POSTGRES_USER")
    DB_PASSWORD = getenv("POSTGRES_PASSWORD")
    SECRET_KEY = getenv("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432"
    )