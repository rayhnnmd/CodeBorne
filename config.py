import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://codeborne.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HACKATIME_CLIENT_ID = os.getenv("HACKATIME_CLIENT_ID")
    HACKATIME_CLIENT_SECRET = os.getenv("HACKATIME_CLIENT_ID")
    HACKATIME_REDIRECT_URI = os.getenv("HACKATIME_REDIRECT_URI", "http://localhost:5000/auth/callback")
    HACKATIME_BASE_URL = "https://hackatime.haclclub.com/api/v1"
    HACKATIME_AUTH_URL = "https://hackatime.hackclub.com/oauth/authorize"
    HACKATIME_TOKEN_URL = "https://hackatime.hackclub.com/oauth/token"