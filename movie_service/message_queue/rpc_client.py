import pika
import uuid
import logging

from message_queue.rmq import configure_logging, get_connection
from app.models.movie import ElasticRequest, ElasticResponse, BaseContractModel

class MovieRpcClient:
    def __init__(self):
        configure_logging()
        self.connection = get_connection()
        self.channel = self.connection.channel()

        # Объявляем постоянную очередь для получения ответов
        self.channel.queue_declare(queue='rpc_response_queue', durable=True)
        self.callback_queue = 'rpc_response_queue'

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            # auto_ack=True,
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, search_request: int) -> BaseContractModel:
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(search_request)
        )

        # Ожидаем ответ
        while self.response is None:
            self.connection.process_data_events(time_limit=None)

        return int(self.response)

if __name__ == "__main__":
    movie_rpc = MovieRpcClient()

    print(" [x] Requesting fib(30)")
    response = movie_rpc.call(30)
    print(f" [.] Got {response}")
