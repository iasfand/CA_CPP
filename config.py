from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("ENV", "DEVT")
    OPENAIP_API_KEY = os.environ.get("OPENAIP_API_KEY")
    OPENAIP_API_URL = os.environ.get("OPENAIP_API_URL")
    AIRPORTDB_API_KEY = os.environ.get("AIRPORTDB_API_KEY")

