import requests
import os

BASE_URL = "http://localhost:8000/files/"
TEST_FILE = "test_image.jpg"
LOCAL_STORAGE_PATH = "./data/media"


def upload_file():
    with open(TEST_FILE, "rb") as file:
        response = requests.post(BASE_URL, files={"file": file})
        if response.status_code == 200:
            print("Файл успешно загружен.")
        else:
            print(f"Ошибка загрузки: {response.status_code} - {response.text}")
        return response


def verify_metadata(response):
    json_response = response.json()
    assert "uid" in json_response, "UID отсутствует в ответе"
    assert "original_name" in json_response, "Оригинальное имя отсутствует в ответе"
    assert "extension" in json_response, "Расширение отсутствует в ответе"
    assert "size" in json_response, "Размер отсутствует в ответе"
    print("Метаданные успешно проверены.")


def verify_local_file(uid, extension):
    file_path = os.path.join(LOCAL_STORAGE_PATH, f"{uid}{extension}")
    assert os.path.exists(file_path), f"Файл {file_path} не найден!"
    print(f"Файл {file_path} успешно сохранён локально.")


def run_tests():
    print("Запуск тестирования...")
    
    # Проверка наличия тестового файла
    assert os.path.exists(TEST_FILE), f"Тестовый файл {TEST_FILE} не найден!"
    
    # Загружаем файл
    response = upload_file()
    
    # Проверяем статус-код
    assert response.status_code == 200, "Ответ от сервера не успешный."
    
    # Проверка метаданных
    verify_metadata(response)
    
    # Проверка локального файла
    uid = response.json()["uid"]
    extension = response.json()["extension"]
    verify_local_file(uid, extension)
    
    print("Все тесты пройдены успешно!")


if __name__ == "__main__":
    run_tests()
