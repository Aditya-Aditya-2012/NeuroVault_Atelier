# backend/src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.src.models.user import User
from backend.src.models.image import Image
from backend.src.db.session import engine
from backend.src.db.base import Base
from backend.src.api import auth, images

# ---------------------------------------------------------
# 🚩 BUG HUNTING ZONE 🚩
# ---------------------------------------------------------
# We want to create tables when the app starts.
# We are importing 'Base' from db.base.
# Does 'db.base' know about the 'User' model? 
# If Python hasn't read the 'models/user.py' file yet,
# Base.metadata will be EMPTY.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown (optional cleanup)

app = FastAPI(title="NeuroVault Atelier", lifespan=lifespan)

# Include our routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(images.router, prefix="/images", tags=["images"])

@app.get("/")
def read_root():
    return {"message": "Welcome to NeuroVault Atelier"}