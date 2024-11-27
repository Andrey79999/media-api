import os

def extract_file_metadata(file) -> dict:
    filename = file.filename
    size = len(file.file.read())
    extension = os.path.splitext(filename)[1]
    return {
        "original_name": filename,
        "size": size,
        "extension": extension.lower(),
        "format": None #TODO: add format
    }
