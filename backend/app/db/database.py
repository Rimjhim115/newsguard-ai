from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from app.config import settings
import os

# Check if DATABASE_URL is provided directly (Render provides this)
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Render provides PostgreSQL URL starting with postgres://
    # SQLAlchemy needs postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
else:
    # Local development — use MySQL
    password = quote_plus(settings.DB_PASSWORD)
    DATABASE_URL = (
        f"mysql+pymysql://{settings.DB_USER}:{password}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()