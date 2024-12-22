from minio import Minio
from minio.error import S3Error
import os

import logging

BASE_URL = "localhost:9000"
MOVIES_BUCKET = "movies"
MOVIES_POSTERS_BUCKET = "posters"
ACCESS_KEY = "minioadmin"
SECRET_KEY = "minioadmin"


class S3Repository:
    def __init__(self):
        """
        MinIO init.
        """
        self.client = Minio(
            BASE_URL,
            access_key=ACCESS_KEY,
            secret_key=SECRET_KEY,
            secure=False
        )
        self.base_url = f"http://{BASE_URL}"

    def file_exists(self, object_name: str) -> bool:
        """
        File exists
        """
        try:
            self.client.stat_object(MOVIES_BUCKET, object_name+'.mp4')
            try:
                self.client.stat_object(MOVIES_POSTERS_BUCKET, object_name+'.jpg')
            except S3Error as err:
                if err.code == "NoSuchKey":
                    logging.info(f"Such movie poster does not exist: {err}")
                return False
            return True
        except S3Error as err:
            if err.code == "NoSuchKey":
                logging.info(f"Such movie does not exist: {err}")
            return False

    def get_url(self, object_name: str) -> dict:
        """
        Generates URLs
        """
        logging.info(f"movie name: {object_name}")
        if not self.file_exists(object_name):
            return dict({
                "movie_url": f"{self.base_url}/{MOVIES_BUCKET}/default-movie.mp4",
                "movie_poster_url": f"{self.base_url}/{MOVIES_POSTERS_BUCKET}/default-poster.png"
            })

        return dict({
            "movie_url": f"{self.base_url}/{MOVIES_BUCKET}/{object_name}.mp4",
            "movie_poster_url": f"{self.base_url}/{MOVIES_POSTERS_BUCKET}/{object_name}.jpg"
        })
