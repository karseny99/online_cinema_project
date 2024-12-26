from minio import Minio
from minio.error import S3Error
import logging
import os

# Конфигурация для подключения к MinIO
BASE_URL = "localhost:9000"
MOVIES_BUCKET = "movies"
MOVIES_POSTERS_BUCKET = "posters"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"

class S3Repository:
    def __init__(self):
        """
        Инициализация MinIO клиента.
        """
        self.client = Minio(
            BASE_URL,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False  # False для работы без HTTPS
        )
        self.base_url = f"http://{BASE_URL}"

    def file_exists(self, bucket_name: str, object_name: str) -> bool:
        """
        Проверка, существует ли объект в бакете.
        """
        try:
            self.client.stat_object(bucket_name, object_name)
            return True
        except S3Error as err:
            if err.code == "NoSuchKey":
                logging.info(f"Файл {object_name} не найден в бакете {bucket_name}: {err}")
            return False

    def get_url(self, bucket_name: str, object_name: str) -> str:
        """
        Генерация прямого URL для объекта.
        """
        try:
            self.file_exists(bucket_name, object_name)
            return f"{self.base_url}/{bucket_name}/{object_name}"
        except S3Error as err:
            logging.error(f"Ошибка при получении URL для {object_name} в бакете {bucket_name}: {err}")
            return ""

    def upload_file(self, bucket_name: str, object_name: str, file_path: str) -> bool:
        """
        Загрузка файла в указанный бакет.
        """
        try:
            if not self.client.bucket_exists(bucket_name):
                logging.info(f"Бакет '{bucket_name}' не существует. Создаем его...")
                self.client.make_bucket(bucket_name)

            self.client.fput_object(bucket_name, object_name, file_path)
            logging.info(f"Файл '{file_path}' успешно загружен в бакет '{bucket_name}' как '{object_name}'.")
            return True
        except S3Error as err:
            logging.error(f"Ошибка при загрузке файла: {err}")
            return False

    def delete_file(self, bucket_name: str, object_name: str) -> bool:
        """
        Удаление файла из указанного бакета.
        """
        try:
            self.client.remove_object(bucket_name, object_name)
            logging.info(f"Файл '{object_name}' успешно удален из бакета '{bucket_name}'.")
            return True
        except S3Error as err:
            logging.error(f"Ошибка при удалении файла {object_name} из бакета {bucket_name}: {err}")
            return False

    def list_files(self, bucket_name: str) -> list:
        """
        Получение списка всех файлов в бакете.
        """
        try:
            objects = self.client.list_objects(bucket_name)
            file_list = [obj.object_name for obj in objects]
            logging.info(f"Список файлов в бакете '{bucket_name}': {file_list}")
            return file_list
        except S3Error as err:
            logging.error(f"Ошибка при получении списка файлов из бакета {bucket_name}: {err}")
            return []
