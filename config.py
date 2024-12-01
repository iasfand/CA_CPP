from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("ENV", "DEVT")
    OPENAIP_API_KEY = os.environ.get("OPENAIP_API_KEY")
    OPENAIP_API_URL = os.environ.get("OPENAIP_API_URL")
    SESSION_SECRET = os.environ.get("SESSION_SECRET")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_SESSION_TOKEN = os.getenv("AWS_SESSION_TOKEN")
    AWS_REGION = os.getenv("AWS_REGION")
    AWS_PROFILE_NAME = os.getenv("AWS_PROFILE_NAME")
    DYNAMODB_TABLE_NAME = "skyport_users"
    DYNAMODB_FAVS_TABLE_NAME = "skyport_favs"
    S3_BUCKET_NAME = "skyport-bucket"
    DYNAMODB_MEMO_TABLE_NAME = "skyport_memories"
