import pika
import time
from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_DLQ,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
    MQ_ROUTING_KEY_RPC_USER_QUEUE,
    MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE,
    MQ_ROUTING_KEY_RPC_AUTH_QUEUE,
    MQ_MESSAGE_TTL,
)

def declare_queues(channel):
    # Объявляем мертвую очередь
    channel.queue_declare(queue=MQ_ROUTING_KEY_DLQ, durable=True)

    args = {
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': 'rpc.dlx',
        'x-dead-letter-routing-key': MQ_ROUTING_KEY_DLQ
    }
    # Объявляем очереди для movie_service
    channel.queue_declare(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, durable=True, arguments=args)

    # Объявляем очереди для auth_service
    channel.queue_declare(queue=MQ_ROUTING_KEY_RPC_AUTH_QUEUE, durable=True, arguments=args)

    # Объявляем очереди для user_service
    channel.queue_declare(queue=MQ_ROUTING_KEY_RPC_USER_QUEUE, durable=True, arguments=args)
    
    # Объявляем очереди для user_service
    channel.queue_declare(queue=MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE, durable=True, arguments=args)


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
    time.sleep(8)  # Ждем, чтобы RabbitMQ успел запуститься
    main()


