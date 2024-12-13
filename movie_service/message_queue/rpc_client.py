import pika
import uuid
import logging
import time

from message_queue.rmq import configure_logging, get_connection
from app.models.movie import ElasticRequest, ElasticResponse, BaseContractModel
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
            host=MQ_HOST,  # Убедитесь, что это имя сервиса в docker-compose
            port=MQ_PORT,
            credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),  # Используйте ваши учетные данные
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

    def call(self, search_request: int) -> BaseContractModel:
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=MQ_ROUTING_KEY_RPC_QUEUE,  # Используем глобальный ключ маршрутизации
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(search_request)
        )

        # Ожидаем ответ
        timeout = time.time() + 6  # Устанавливаем время ожидания в 6 секунд
        while self.response is None:
            # Проверяем, не истекло ли время ожидания
            if time.time() > timeout:
                print(" [!] No response received, moving to the next request.")
                break  # Выходим из цикла, если время ожидания истекло
            self.connection.process_data_events(time_limit=1)  # Обрабатываем события

        return int(self.response)

def main():
    movie_rpc = MovieRpcClient()

    i = 1
    while True:
        print(f" [x] Requesting fib({i})")
        response = movie_rpc.call(i)
        if response is not None:
            print(f" [.] Got {response}")
        else:
            print(" [.] No response received.")
        time.sleep(1)  # Задержка перед следующим запросом
        i += 1

if __name__ == "__main__":
    main()
