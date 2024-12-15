from celery import Celery
from pydantic import BaseModel
from kombu import Queue
import random
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
    MQ_MESSAGE_TTL,
)

app = Celery('client', 
    broker=f'pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}//', # Тип брокера (Rabbit в нашем случае)
    backend='rpc://', # хуй знает, но надо
    # tasks_routes={"tasks.process_message", MQ_ROUTING_KEY_RPC_MOVIE_QUEUE},
)

# настройка для исполбзуемой очереди
app.conf.task_queues = (
    Queue(MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, routing_key=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, queue_arguments={
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': 'rpc.dlx',
        'x-dead-letter-routing-key': 'rpc_dlq'
    }),
)

class MessageModel(BaseModel):
    text: str
    sender: str
# Создание экземпляра модели

message = MessageModel(text="Hello, RPC!", sender="User1")

# Отправка сообщения через RPC
result = app.send_task(
    'tasks.process_message', # Название функции в сервисе (tasks - имя файла, process_message - название функции)
    args=[message.model_dump()],
    queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,    
)

# Получение результата
try:
    response = result.get(timeout=10)  # Ожидание результата до 10 секунд + пришлет именно тому, кто запрашивал, corr_id не нужен
    print('Response:', response)
except Exception as e:
    print(f"An error occurred: {e}")
