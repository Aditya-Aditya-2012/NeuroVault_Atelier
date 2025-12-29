# backend/src/main.py
from contextlib import asynccontextmanager
from backend.src.tasks.ai_tasks import GENERATED_DIR
from fastapi import FastAPI
from backend.src.models.user import User
from backend.src.models.image import Image
from backend.src.db.session import engine
from backend.src.db.base import Base
from backend.src.api import auth, images
from fastapi.staticfiles import StaticFiles
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (optional cleanup)

app = FastAPI(title="NeuroVault Atelier", lifespan=lifespan)

GENERATED_DIR = Path("backend/data/generated")
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=str(GENERATED_DIR)), name="outputs")
# Include our routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
def read_root():
    return {"message": "Welcome to NeuroVault Atelier"}