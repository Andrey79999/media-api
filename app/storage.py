import os
import shutil
from uuid import uuid4

STORAGE_PATH = "/media"

os.makedirs(STORAGE_PATH, exist_ok=True)

def save_file_locally(file, filename: str) -> str:
    file_path = os.path.join(STORAGE_PATH, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path

def generate_uid() -> str:
    return str(uuid4())

async def send_to_cloud(file_path: str):
    ...
