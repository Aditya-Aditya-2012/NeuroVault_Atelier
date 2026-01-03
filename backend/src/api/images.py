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
from backend.src.models.output import Output
from backend.src.models.task import AITask, TaskStatus
from backend.src.tasks.ai_tasks import auto_tag_image_task, process_landscape_task, process_multi_alchemy
from sqlalchemy import select
from collections import defaultdict
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

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
        owner_id = current_user.id 
    )
    db.add(new_image)

    try:
        await db.commit()
        await db.refresh(new_image)
        #process_landscape_task.apply_async(args=[new_image.id], queue="ai_queue")
        auto_tag_image_task.apply_async(args=[new_image.id], queue="ai_queue")
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

@router.get("/{image_id}/status")
async def get_image_status(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Image).where(Image.id == image_id, Image.owner_id == current_user.id)
    )
    image = result.scalars().first()

    # If no image found, raise 404
    if not image:
        raise HTTPException(status_code=404, detail="Image not found or access denied")

    return {
        "id": image_id,
        "filename": image.filename,
        "is_processed": image.is_processed,
        "keywords": image.keywords
    }

@router.post("/alchemy")
async def create_alchemy_task(
    image_ids: list[int],
    prompt: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if len(image_ids) > 3:
        raise HTTPException(status_code=400, detail="Maximum 3 images allowed")
    
    result = await db.execute(
        select(Image).where(Image.id.in_(image_ids))
    )
    found_images = result.scalars().all()

    if len(found_images) != len(image_ids):
        raise HTTPException(status_code=404, detail="One or more images not found")
    
    for images in found_images:
        if images.owner_id != current_user.id :
            raise HTTPException(status_code=404, detail="Unauthorized")
    
    new_task = AITask(
        user_id = current_user.id, 
        input_image_ids = image_ids,
        prompt = prompt,
        status=TaskStatus.PENDING
    )
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    process_multi_alchemy.apply_async(args=[new_task.id], queue="ai_queue")

    return {"task_id": new_task.id, "status": new_task.status}

@router.get("/search/{keyword}")
async def search_by_keyword(
    keyword: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Image).where(Image.keywords.any(keyword), Image.owner_id == current_user.id)
    )
    found_images = result.scalars().all()

    if not found_images:
        raise HTTPException(status=404, detail=f"Images with keyword:{keyword} not found")
    
    return {
        "count": len(found_images),
        "results":[
            {
                "id": img.id,
                "filename": img.filename,
                "created_at": img.created_at.isoformat(),
                "keywords": img.keywords
            } for img in found_images
        ]
    }

@router.get("/{image_id}/history")
async def get_image_history(
    image_id : int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Image).where(Image.id == image_id, Image.owner_id == current_user.id)
    )

    image = result.scalars().first()

    if not image:
        raise HTTPException(status_code=404, detail="image not found or access denied")
    
    res_outputs = await db.execute(
        select(Output).where(Output.source_filenames.any(image.file_path))
    )

    outputs = res_outputs.scalars().all()

    return {
        "original_id": {image_id},
        "generatedimages": [output.gen_file_path for output in outputs]
        }

@router.get("/gallery")
async def get_full_gallery(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Image).where(Image.owner_id == current_user.id)
    )
    images = result.scalars().all()

    if not images:
        print(f"you have no images currently")
        return []

    all_paths = [img.file_path for img in images]

    out_result = await db.execute(
        select(Output).where(Output.source_filenames.cast(PG_ARRAY(String)).overlap(all_paths))
    )

    outputs = out_result.scalars().all()

    output_map = defaultdict(list)
    for out in outputs:
        for path in out.source_filenames:
            output_map[path].append(out.gen_file_path)
    
    gallery_data = [
        {
            "id": img.id,
            "original": img.file_path,
            "keywords": img.keywords,
            "ai_versions": output_map.get(img.file_path, [])
        }
        for img in images
    ]

    return gallery_data
