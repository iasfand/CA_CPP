import os

class Config:
    SECRET_KEY = os.environ.get("ENV", "DEVT")
