from core.minio_client import MinioClient

class MovieRepository:
    def __init__(self):
        self.minio_client = MinioClient()

    def get_movie_url(self, movie_name: str) -> str:
        """Получить временную ссылку на фильм."""
        return self.minio_client.get_presigned_url(movie_name)
