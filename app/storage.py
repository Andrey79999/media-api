import os
import shutil
from uuid import uuid4
from logger import logger

import aioboto3
from utils import get_aws_access_keys

STORAGE_PATH = "/media"

os.makedirs(STORAGE_PATH, exist_ok=True)


def save_file_locally(file, filename: str) -> str:
    file_path = os.path.join(STORAGE_PATH, filename)
    file.file.seek(0)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_path


def generate_uid() -> str:
    return str(uuid4())


async def send_to_cloud(filename: str, bucket: str):
    try:
        logger.info(f"Starting upload of file '{filename}' to bucket '{bucket}'.")

        aws_access_key_id, aws_secret_access_key = get_aws_access_keys()

        file_path = os.path.join(STORAGE_PATH, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        session = aioboto3.Session()
        async with session.client(
                service_name='s3',
                region_name='ru-central1',
                endpoint_url='https://storage.yandexcloud.net',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
        ) as s3:
            with open(file_path, "rb") as data:
                await s3.upload_fileobj(data, bucket, filename)
            logger.info(f"File uploaded successfully: {file_path} -> {bucket}/{filename}")
    except FileNotFoundError as e:
        logger.error(f"File error: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during file upload: {e}")
