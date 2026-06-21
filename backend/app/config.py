# backend/app/config.py
# PURPOSE: Central configuration management.
# Pydantic-settings reads from your .env file and validates
# that all required variables are present.
# If SECRET_KEY is missing from .env, the app won't start
# at all — failing loudly is better than failing silently.

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_PORT: int = 3306
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    APP_ENV: str = "development"
    YOUTUBE_API_KEY: str = "AIzaSyB6Uyh75TM1qdDd4xj3Tk4m12UAW3EPOfU"

    class Config:
        env_file = ".env"  # Tells pydantic where to read from


# Create a single instance — imported everywhere else
# This is the Singleton pattern
settings = Settings()