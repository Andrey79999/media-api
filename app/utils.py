import os
import mimetypes


def extract_file_metadata(file) -> dict:
    filename = file.filename
    size = len(file.file.read())
    extension = os.path.splitext(filename)[1]
    return {
        "original_name": filename,
        "size": size,
        "extension": extension.lower(),
        "format": get_file_mime_type(filename)
    }


def get_file_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type


def get_aws_access_keys() -> (str, str):
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    if aws_secret_access_key is not None and aws_access_key_id is not None:
        return aws_access_key_id, aws_secret_access_key
    else:
        raise ValueError('AWS_SECRET_ACCESS_KEY or AWS_ACCESS_KEY_ID environment variable not set')
