import requests
import os
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://localhost:8000/files/"
LOCAL_STORAGE_PATH = "./data/media"
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
