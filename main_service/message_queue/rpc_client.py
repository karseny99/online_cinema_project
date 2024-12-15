import pika
import uuid
import time
import json

from models.models import BaseContractModel
from models.user_service_models import  SetMovieRatingRequest

from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_RPC_QUEUE,
    MQ_ROUTING_KEY_RPC_RESPONSE_QUEUE,
)

class MovieRpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=MQ_HOST,  # это имя сервиса в docker-compose
            port=MQ_PORT,
            credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
        ))
        self.channel = self.connection.channel()

        self.callback_queue = MQ_ROUTING_KEY_RPC_RESPONSE_QUEUE

        # self.channel.queue_declare(queue=self.callback_queue, durable=True)  # Объявляем очередь для ответов
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=False,  # Устанавливаем auto_ack в False для ручного подтверждения
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def call(self, set_rating_request: SetMovieRatingRequest) -> BaseContractModel:
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # Сериализуем объект в JSON
        request_json = json.dumps(set_rating_request.__dict__)

        self.channel.basic_publish(
            exchange='',
            routing_key=MQ_ROUTING_KEY_RPC_QUEUE,  # Используем глобальный ключ маршрутизации
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request_json
        )

        # Ожидаем ответ
        timeout = time.time() + 6  # Устанавливаем время ожидания в 6 секунд
        while self.response is None:
            # Проверяем, не истекло ли время ожидания
            if time.time() > timeout:
                print(" [!] No response received, moving to the next request.")
                break  # Выходим из цикла, если время ожидания истекло
            self.connection.process_data_events(time_limit=1)  # Обрабатываем события

        if self.response:
            return json.loads(self.response)

        return None

def main():
    movie_rpc = MovieRpcClient()

    set_rating = SetMovieRatingRequest(
        movie_id=1,
        user_id=5,
        rating=4.1
    )
    while True:
        set_rating.rating += 0.1
        print(f" [x] Requesting set_rating({set_rating})")
        response = movie_rpc.call(set_rating)
        if response is not None:
            print(f" [.] Got {response}")
        else:
            print(" [.] No response received.")
        time.sleep(1)  # Задержка перед следующим запросом

if __name__ == "__main__":
    main()