from celery import Celery
from pydantic import BaseModel
from kombu import Queue
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
    MQ_MESSAGE_TTL,
)


app = Celery(
    'tasks', 
    broker=f'pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}//', 
    backend='rpc://',
    queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
)

app.conf.worker_prefetch_multiplier = 1 # Воркер будет брать одну задачу за раз
app.conf.task_queues = (
    Queue(MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, 
    routing_key=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, 
    queue_arguments=
    {
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': 'rpc.dlx', 
        'x-dead-letter-routing-key': 'rpc_dlq'
    }),
)


class MessageModel(BaseModel):
    text: str
    sender: str


@app.task(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE)
def process_message(message_data):
    message = MessageModel(**message_data)  # Восстановление модели Pydantic
    # Обработка сообщения
    return f"Received message from {message.sender}: {message.text}" # 


# from celery import shared_task

# @shared_task
# def process_message(message):
#     try:
#         # Логика обработки сообщения
#         print(f"Processing message from {message['sender']}: {message['text']}")
#         # Если что-то пошло не так, выбросьте исключение
#         if some_condition:  # Замените на вашу логику
#             raise Exception("Error processing message")
#     except Exception as e:
#         # Логирование ошибки
#         print(f"Error: {e}")
#         raise  # Это отправит сообщение в мертвую очередь
