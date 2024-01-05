import os

from dotenv import load_dotenv

load_dotenv()
ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:3000",
]
APP_HOST = os.environ.get('APP_HOST')
APP_PORT = os.environ.get('APP_PORT')

DB_USER = os.environ.get('PGUSER')
DB_PASS = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
SECRET = os.environ.get('SECRET') or 'ofjsdiofjio3jio43orfweogoi3hth34t'
