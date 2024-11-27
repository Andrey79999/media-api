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
