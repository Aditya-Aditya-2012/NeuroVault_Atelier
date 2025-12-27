import time
from backend.src.core.celery_app import celery_app
from backend.src.db.session import SQLALCHEMY_DATABASE_URL
from fastapi.background import P
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.models.image import Image
from backend.src.models.user import User

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
    db=SessionLocal()
    try:
        time.sleep(10)
        image=db.query(Image).filter(Image.id == image_id).first()

        if image:
            image.is_processed = True
            db.commit()
            print("db updated for Image ID: {image_id}")
        else:
            print(f"Image not found")
    except Exception as e:
        print(f"Error during AI task: {e}")
        db.rollback()
    finally:
        db.close()

    return {"status": "success", "image_id": image_id}