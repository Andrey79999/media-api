from pydantic import BaseModel

class FileMetadataCreate(BaseModel):
    original_name: str
    extension: str
    size: float
    format: str | None

class FileMetadataResponse(FileMetadataCreate):
    uid: str

    class Config:
        orm_mode = True
