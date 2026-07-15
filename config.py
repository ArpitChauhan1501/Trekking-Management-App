import os

class Config:
    SECRET_KEY = "63926e0f2b6d6d60cae441b2df4eb9a4"

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///trekking.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
