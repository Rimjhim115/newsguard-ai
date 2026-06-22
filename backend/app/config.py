# backend/app/config.py
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

    # YouTube API
    YOUTUBE_API_KEY: str = ""    # ← this was missing

    class Config:
        env_file = ".env"


settings = Settings()