from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import engine
from app.db import models
from app.api.v1 import auth, predictions, users
from app.ml.model import classifier

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading ML model...")
    classifier.load()
    yield
    print("Shutting down...")

app = FastAPI(
    title="NewsGuard AI",
    description="Full-Stack News Verification Platform",
    version="1.0.0",
    lifespan=lifespan
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost",
        "https://newsguard-ai.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(predictions.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "NewsGuard AI"}