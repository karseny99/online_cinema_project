import pika
import time
from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_DLQ,
    MQ_ROUTING_KEY_RPC_QUEUE,
    MQ_ROUTING_KEY_RPC_RESPONSE_QUEUE,
    MQ_MESSAGE_TTL,
)

def declare_queues(channel):
    # Объявляем мертвую очередь
    channel.queue_declare(queue=MQ_ROUTING_KEY_DLQ, durable=True)

    # Объявляем user_service очередь для запросов
    args_request = {
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': '',
        'x-dead-letter-routing-key': MQ_ROUTING_KEY_DLQ
    }
    channel.queue_declare(queue=MQ_ROUTING_KEY_RPC_QUEUE, durable=True, arguments=args_request)

    # Объявляем user_service очередь для ответов
    args_response = {
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': '',
        'x-dead-letter-routing-key': MQ_ROUTING_KEY_DLQ
    }
    channel.queue_declare(queue=MQ_ROUTING_KEY_RPC_RESPONSE_QUEUE, durable=True, arguments=args_response)

def main():
    connection_params = pika.ConnectionParameters(
        host=MQ_HOST,
        port=MQ_PORT,
        credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    declare_queues(channel)
    connection.close()

if __name__ == "__main__":
    time.sleep(5)  # Ждем, чтобы RabbitMQ успел запуститься
    main()


# TODO:
# Это файл инициализации очереди, он будет запускаться вместе с запуском контейнера с очередью
# Соответственно для rpc server и rpc client надо будет прописать получение коннекшена
# Докерфайл и настройка в гпт