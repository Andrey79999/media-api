import requests
import os
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000/files/"
LOCAL_STORAGE_PATH = "./data/media"
TEST_DOWNLOAD_PATH = "./data/test_downloads"
MAX_WORKERS = 5  # Максимальное число параллельных загрузок


def upload_file(test_file):
    """
    Загружает файл на сервер и возвращает ответ.
    """
    try:
        with open(test_file, "rb") as file:
            response = requests.post(BASE_URL, files={"file": file})
            if response.status_code == 200:
                print(f"[SUCCESS] Файл {test_file} успешно загружен.")
            else:
                print(f"[ERROR] Ошибка загрузки {test_file}: {response.status_code} - {response.text}")
            return test_file, response
    except Exception as e:
        print(f"[EXCEPTION] Ошибка при загрузке {test_file}: {e}")
        return test_file, None


def verify_metadata(response, test_file):
    """
    Проверяет метаданные в ответе от API.
    """
    try:
        json_response = response.json()
        assert "uid" in json_response, "UID отсутствует в ответе"
        assert "original_name" in json_response, "Оригинальное имя отсутствует в ответе"
        assert "extension" in json_response, "Расширение отсутствует в ответе"
        assert "size" in json_response, "Размер отсутствует в ответе"
        print(f"[VERIFY] Метаданные {test_file} успешно проверены.")
    except AssertionError as e:
        print(f"[ERROR] Ошибка в метаданных {test_file}: {e}")
    except Exception as e:
        print(f"[EXCEPTION] Невозможно проверить метаданные {test_file}: {e}")


def verify_local_file(uid, extension, test_file):
    """
    Проверяет наличие файла в локальном хранилище.
    """
    try:
        file_path = os.path.join(LOCAL_STORAGE_PATH, f"{uid}{extension}")
        assert os.path.exists(file_path), f"Файл {file_path} не найден!"
        print(f"[VERIFY] Локальный файл {test_file} успешно сохранён.")
    except AssertionError as e:
        print(f"[ERROR] Локальный файл {test_file} отсутствует: {e}")


def verify_downloaded_file(original_file, downloaded_file):
    """
    Сравнивает оригинальный и скачанный файл по размеру.
    """
    try:
        assert os.path.exists(downloaded_file), "Скачанный файл отсутствует!"
        assert os.path.getsize(original_file) == os.path.getsize(downloaded_file), \
            "Размеры оригинального и скачанного файла не совпадают!"
        print(f"[VERIFY] Скачанный файл {downloaded_file} успешно проверен.")
    except AssertionError as e:
        print(f"[ERROR] Ошибка при проверке скачанного файла: {e}")


def download_file(uid, test_file):
    """
    Загружает файл с сервера по UID.
    """
    try:
        download_path = os.path.join(TEST_DOWNLOAD_PATH, f"{uid}_downloaded")
        response = requests.get(f"{BASE_URL}{uid}", stream=True)
        if response.status_code == 200:
            os.makedirs(TEST_DOWNLOAD_PATH, exist_ok=True)
            with open(download_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"[SUCCESS] Файл {test_file} успешно скачан: {download_path}")
            return download_path
        else:
            print(f"[ERROR] Ошибка скачивания {test_file}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"[EXCEPTION] Ошибка при скачивании {test_file}: {e}")
        return None


def process_file(test_file):
    """
    Обрабатывает загрузку и верификацию для одного файла.
    """
    response = upload_file(test_file)[1]
    if response and response.status_code == 200:
        verify_metadata(response, test_file)
        uid = response.json()["uid"]
        extension = response.json()["extension"]
        verify_local_file(uid, extension, test_file)

        downloaded_file = download_file(uid, test_file)
        if downloaded_file:
            verify_downloaded_file(test_file, downloaded_file)


def run_tests():
    """
    Запускает параллельное тестирование для всех тестовых файлов.
    """
    print("Запуск тестирования...")

    test_files = [file for file in os.listdir() if file.startswith("test_file")]
    assert test_files, "Тестовые файлы отсутствуют в директории!"

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_file, test_files)

    print("Все тесты завершены!")


if __name__ == "__main__":
    run_tests()
