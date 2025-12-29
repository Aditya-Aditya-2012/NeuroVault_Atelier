from email.mime import image
import time
import os
import uuid
from pathlib import Path
from backend.src.core.celery_app import celery_app
from backend.src.db.session import SQLALCHEMY_DATABASE_URL
from fastapi.background import P
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.src.models.image import Image
from backend.src.models.user import User
from backend.src.models.task import AITask, TaskStatus
from backend.src.models.output import Output
from PIL import Image as PILImage

SYNC_DB_URL = SQLALCHEMY_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
GENERATED_DIR = Path("backend/data/generated")

if GENERATED_DIR.is_dir() == False:
    GENERATED_DIR.mkdir(parents=True, exist_ok=True)

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
        img_record = db.query(Image).filter(Image.id == image_id).first()
        if not img_record:
            print("Error: Image not found")
            return
        
        with PILImage.open(img_record.file_path) as img:
            processed_img = img.convert('L') 
            unique_id = uuid.uuid4().hex
            output_filename = f"{unique_id}_grayscale_{img_record.filename}"
            output_path = GENERATED_DIR / output_filename
            processed_img.save(output_path)
        
        img_record.is_processed = True
        db.commit()
        print(f"Success, Saved to {output_path}")

    except Exception as e:
        print(f"Transformation failed: {e}")
        db.rollback()
    finally:
        db.close()

@celery_app.task(name="process_multi_alchemy")
def process_multi_alchemy(task_id: int):
    db = SessionLocal()
    try:
        task = db.query(AITask).filter(AITask.id == task_id).first()
        if not task: return

        images = db.query(Image).filter(Image.id.in_(task.input_image_ids))

        pil_images = [PILImage.open(img.file_path) for img in images]

        total_width = sum(i.width for i in pil_images)
        max_height = max(i.height for i in pil_images)

        canvas = PILImage.new('RGB', (total_width, max_height))

        x_offset = 0
        for p_img in pil_images:
            canvas.paste(p_img, (x_offset, 0))
            x_offset += p_img.width
        
        output_filename = f"alchemy_{task_id}.jpg"
        output_path = GENERATED_DIR / output_filename
        canvas.save(output_path)

        #TODO: Populate the 'Outputs' table!
        # Create output table and models for it
        array_path=[]
        for img in images:
            array_path.append(img.file_path)

        task.status = TaskStatus.COMPLETED

        generated_img = Output(
            task_id = task_id,
            gen_file_path = str(output_path),
            source_filenames = array_path, 
        )
        db.add(generated_img)
        db.commit()
        db.refresh(generated_img)
        print(f"Alchemy successful, generated image at {output_path}")
    except Exception as e:
        print(f"Alchemy failed: {e}")
        task.status = TaskStatus.FAILED
        db.commit()
    finally:
        db.close()