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
from fastapi.middleware.cors import CORSMiddleware

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (optional cleanup)

app = FastAPI(title="NeuroVault Atelier", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


GENERATED_DIR = Path("backend/data/uploads")
GENERATED_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=str(GENERATED_DIR)), name="uploads")
# Include our routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
def read_root():
    return {"message": "Welcome to NeuroVault Atelier"}