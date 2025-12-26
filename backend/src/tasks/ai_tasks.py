import time
from backend.src.core.celery_app import celery_app
from backend.src.db.session import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SYNC_DB_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

engine = create_engine(SYNC_DB_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine,
)

@celery_app.task(name="process_landscape")
def process_landscape_task(image_id: int):
    """
    Simulates Stable Diffusion Processing
    """

    print(f"Starting AI generation for Image ID: {image_id}")

    time.sleep(10)

    db=SessionLocal()

    print(f"AI Generation Complete for ID: {image_id}")
    return {"status": "success", "image_id": image_id}