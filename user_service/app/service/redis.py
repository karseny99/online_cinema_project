import redis
from pydantic import BaseModel
import json


class RedisClient:

    def __init__(
            self,
            REDIS_HOST: str = 'localhost',
            REDIS_PORT: int = 6379,
            REDIS_PASSWORD: str = None,
            REDIS_DB: int = 0
    ):

        self.redis_client = redis.StrictRedis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password=REDIS_PASSWORD,
            db=REDIS_DB,
            decode_responses=True  # Декодировать ответы в строки
        )

    def get(self, cache_key: str) -> dict:
        '''
            Returns serialized cached data from redis
            None if unexisted key or redis is unavailable
        '''
        try:
            # Проверка кэша
            cached_result = self.redis_client.get(cache_key)
            if cached_result:
                print(f"Found in cache, returning {cached_result}")
                return json.loads(cached_result)  # Возвращаем результат из кэша
            print(f"Cached value not found: {cache_key}")
        except redis.ConnectionError:
            # Обработка ошибки подключения к Redis
            print("Redis connection error in get method")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from cache: {e}")
        except Exception as e:
            # Обработка других возможных исключений
            print(f"Redis_client error occured: {e}")

        return None

    def set(self, cache_key: str, cache_data: dict, expires: int) -> bool:
        '''
            Returns save-status: true or false
        '''

        try:
            self.redis_client.set(cache_key, json.dumps(cache_data), ex=expires)

            print(f"Successfully saved result in cache by {cache_key}")
            return True
        except ConnectionError:
            print("Redis connection error in set method")
        except Exception as e:
            print(f"Redis_client error occured: {e}")

        return False
