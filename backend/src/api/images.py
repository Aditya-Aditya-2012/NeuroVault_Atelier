from fileinput import filename
import os
import shutil
import uuid
from pathlib import Path
from backend.src.api.deps import get_current_user
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.db.session import get_db
from backend.src.models.image import Image
from backend.src.models.user import User
from backend.src.tasks.ai_tasks import process_landscape_task
from sqlalchemy import select

router = APIRouter()

UPLOAD_DIR = Path("backend/data/uploads")

@router.post("/upload")
async def upload_landscape(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Sanitize filename: strip path info and take only the name
    base_name = os.path.basename(file.filename)
    unique_id = uuid.uuid4().hex
    filename = f"{unique_id}_{base_name}"
    file_location = UPLOAD_DIR / filename

    # Using context manager to ensure file closes automatically
    with open(file_location, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Save to DB
    new_image = Image(
        filename = filename,
        file_path = str(file_location),
        owner_id = current_user.id #hardcoded for now until we fix auth dependency
    )
    db.add(new_image)

    try:
        await db.commit()
        await db.refresh(new_image)
        process_landscape_task.delay(new_image.id)
        return {
            "id": new_image.id, 
            "filename": filename,
            "status": "Processing"
            }
    except:
        os.remove(file_location)
    

@router.get("/my-images")
async def get_my_images(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Image).where(Image.owner_id == current_user.id))
    images = result.scalars().all()

    return images
