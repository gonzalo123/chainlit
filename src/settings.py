import os
from datetime import timedelta
from pathlib import Path
import redis

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
load_dotenv(dotenv_path=BASE_DIR / 'env' / ENVIRONMENT / '.env')

APP_ID = 'chainlit'
SECRET = 'f6b91091faf1b58d1e19e3ade11a78eb'

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

SESSION = dict(
    PERMANENT_SESSION_LIFETIME=os.getenv('PERMANENT_SESSION_LIFETIME', 86400),
    SESSION_PERMANENT=os.getenv('SESSION_PERMANENT', 'True') == 'True',
    SESSION_REFRESH_EACH_REQUEST=os.getenv('SESSION_REFRESH_EACH_REQUEST', 'True') == 'True',
    SESSION_TYPE=os.getenv('SESSION_TYPE', 'redis'),
    SESSION_COOKIE_SECURE=os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True',
    SESSION_COOKIE_PATH=os.getenv('SESSION_COOKIE_PATH', '/'),
    SESSION_COOKIE_HTTPONLY=os.getenv('SESSION_COOKIE_HTTPONLY', 'True') == 'True',
    SESSION_COOKIE_SAMESITE=os.getenv('SESSION_COOKIE_SAMESITE', 'Lax'),
    SESSION_COOKIE_DOMAIN=os.getenv('SESSION_COOKIE_DOMAIN', 'localhost'),
    SESSION_COOKIE_NAME=os.getenv('SESSION_COOKIE_NAME', f'sessionid_{APP_ID}'),
    SESSION_REDIS=redis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}'),
)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

IA_MODEL = "eu.anthropic.claude-sonnet-4-20250514-v1:0"
IA_TEMPERATURE = 0.3

LLM_READ_TIMEOUT = 300
LLM_CONNECT_TIMEOUT = 60
LLM_MAX_ATTEMPTS = 10

JWT_EXPIRATION_TIMEDELTA = timedelta(minutes=1)
JWT_ALGORITHM = "HS256"

MY_LATITUDE = float(os.getenv('MY_LATITUDE'))
MY_LONGITUDE = float(os.getenv('MY_LONGITUDE'))
