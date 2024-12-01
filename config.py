from dotenv import load_dotenv
import os

load_dotenv()

os.environ['AWS_SHARED_CREDENTIALS_FILE'] = './.aws/credentials'
os.environ['AWS_CONFIG_FILE'] = './.aws/config'

class Config:
    # General App Configuration
    MODE = os.environ.get("MODE", "DEVT")
    FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT", 5000)
    OPENAIP_API_KEY = os.environ.get("OPENAIP_API_KEY")
    OPENAIP_API_URL = os.environ.get("OPENAIP_API_URL")
    SESSION_SECRET = os.environ.get("SESSION_SECRET")

    # AWS Credentials and Configuration
    AWS_PROFILE_NAME = os.getenv("AWS_PROFILE_NAME", "250738637992_MSCCLOUD")
    AWS_REGION = os.getenv("AWS_REGION", "eu-west-1")

    # AWS Services Configuration
    DYNAMODB_USER_TABLE_NAME = os.getenv("DYNAMODB_USER_TABLE_NAME", "skyport_users")
    DYNAMODB_FAVS_TABLE_NAME = os.getenv("DYNAMODB_FAVS_TABLE_NAME", "skyport_favs")
    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "skyport-bucket")
    DYNAMODB_MEMO_TABLE_NAME = os.getenv("DYNAMODB_MEMO_TABLE_NAME", "skyport_memories")