import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Needed for sessions (Flask-Login relies on this).
    # In production, set this via an environment variable instead of hardcoding it.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this-in-production")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(BASE_DIR, "instance", "jobs.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False