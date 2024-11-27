from sqlalchemy import Column, Integer, String, Float
from database import Base

class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    uid = Column(String, unique=True, index=True)
    original_name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    size = Column(Float, nullable=False)
    format = Column(String, nullable=True)
