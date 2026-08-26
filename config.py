
import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-secret-key-change-this-in-production"
    )

    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql+psycopg://"
        ).replace(
            "postgresql://", "postgresql+psycopg://"
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or (
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "jobs.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
