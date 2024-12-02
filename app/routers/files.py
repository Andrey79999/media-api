import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import FileMetadata
from schemas import FileMetadataResponse
from storage import save_file_locally, generate_uid, send_to_cloud
from utils import get_file_mime_type
from logger import logger
from aiofiles import open as aio_open


router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/", response_model=FileMetadataResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info("Start uploading file")
    try:
        uid = generate_uid()
        extension = os.path.splitext(file.filename)[1]
        local_file_path = f"/media/{uid}{extension.lower()}"

        async with aio_open(local_file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):
                await out_file.write(content)

        file_size = os.path.getsize(local_file_path)
        mime_type = get_file_mime_type(file.filename)
        db_file = FileMetadata(
            uid=uid,
            original_name=file.filename,
            extension=extension.lower(),
            size=file_size,
            format=mime_type,
        )
        db.add(db_file)
        db.commit()
        db.refresh(db_file)

        await send_to_cloud(filename=local_file_path, bucket=os.getenv('S3BUCKET'))
        logger.info("Finish uploading file")
        return db_file
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Error uploading file")
