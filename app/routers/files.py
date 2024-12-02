import os
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from aiofiles import open as aio_open
from database import get_db
from models import FileMetadata
from schemas import FileMetadataResponse
from storage import generate_uid, send_to_cloud, fetch_from_cloud
from utils import get_file_mime_type
from logger import logger

from fastapi.responses import FileResponse
from starlette.background import BackgroundTasks
from starlette.status import HTTP_404_NOT_FOUND

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/", response_model=FileMetadataResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    logger.info(f"Start uploading file {file.filename}")
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
        logger.info(f"Finish uploading file {file.filename}")
        return db_file
    except HTTPException as e:
        logger.warning(f"HTTP Exception: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail="Error uploading file")


@router.get("/{uid}", response_class=FileResponse)
async def get_file(
        uid: str,
        db: Session = Depends(get_db),
        background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Получить файл по UID.
    Сначала ищет локально, если не найден, то скачивает из S3.
    """
    file_metadata = db.query(FileMetadata).filter(FileMetadata.uid == uid).first()
    if not file_metadata:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="File not found")

    local_file_path = f"/media/{uid}{file_metadata.extension}"

    if os.path.exists(local_file_path):
        return FileResponse(local_file_path, media_type=file_metadata.format, filename=file_metadata.original_name)

    # Если файла нет, пытаемся скачать из S3
    try:
        logger.info(f"File not found locally, fetching from S3: {uid}")
        await fetch_from_cloud(
            bucket=os.getenv('S3BUCKET'),
            filename=f"{uid}{file_metadata.extension}",
            destination=local_file_path
        )
        return FileResponse(local_file_path, media_type=file_metadata.format, filename=file_metadata.original_name)
    except Exception as e:
        logger.error(f"Error fetching file from S3: {e}")
        raise HTTPException(status_code=500, detail="Error fetching file from storage")
