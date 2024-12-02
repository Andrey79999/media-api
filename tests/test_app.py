import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_file_success():
    """
    upload test
    """
    response = client.post(
        "/files/",
        files={"file": ("test.txt", b"sample data")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "uid" in data
    assert data["original_name"] == "test.txt"


def test_upload_file_invalid():
    """
    Test download without file.
    """
    response = client.post("/files/")
    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_file_success():
    """
    Test of successful file retrieval by UID.
    """
    upload_response = client.post(
        "/files/",
        files={"file": ("test.txt", b"sample data")},
    )
    uid = upload_response.json()["uid"]

    response = client.get(f"/files/{uid}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"


def test_get_file_not_found():
    """
    Test for getting a non-existent file.
    """
    response = client.get("/files/nonexistent_uid")
    assert response.status_code == 404
    assert response.json()["detail"] == "File not found"


def test_cleanup_script():
    """
    Testing the correctness of the cleaning script (clear_disk.sh).
    """
    directory = "./data/media"
    if not os.path.exists(directory):
        os.makedirs(directory)

    test_file = os.path.join(directory, "old_file.txt")
    with open(test_file, "w") as f:
        f.write("test")
    os.utime(test_file, (0, 0))

    os.system("bash clear_disk.sh")

    assert not os.path.exists(test_file)
