import os

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import FileMetadata
from schemas import FileMetadataResponse
from storage import save_file_locally, generate_uid, send_to_cloud
from utils import extract_file_metadata

router = APIRouter(prefix="/files", tags=["Files"])


@router.post("/", response_model=FileMetadataResponse)
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    uid = generate_uid()
    file_metadata = extract_file_metadata(file)
    local_file_path = save_file_locally(file, f"{uid}{file_metadata['extension']}")

    db_file = FileMetadata(uid=uid, **file_metadata)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    await send_to_cloud(filename=local_file_path, bucket=os.getenv('S3BUCKET'))

    return db_file
