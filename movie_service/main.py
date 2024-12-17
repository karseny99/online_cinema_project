# from app.elastic_service.elastic_search import elastic_search
# import asyncio

# example_query = ElasticRequest(
#     contract_type=
#     title="Inception", 
#     year=None, 
#     genre=None, 
#     director="Christopher Nolan",
#     page=1,         
#     page_size=10   
# )

# search_query = {
#     "title": "Inception",
#     "year": 2010,
#     "genre": ["Sci-Fi"], # Also as select box   
#     "director": "Christopher Nolan", # Should be as selection in front
#     "page": 1,
#     "page_size": 10
# }

# incoming_message = BaseContractModel(
#     contract_type="search_request",
#     body={
#         "title": "Inception",
#         "year": 2010,
#         "genre": ["Action", "Sci-Fi"],
#         "director": "Christopher Nolan",
#         "page": 1,
#         "page_size": 10
#     }
# )


 

# if __name__ == "__main__":
#     asyncio.run(elastic_search(parse_search_request(incoming_message)))


# from message_queue.rpc_client import *

# if __name__ == "__main__":
#     main()



from celery import Celery
from pydantic import BaseModel
from kombu import Queue
from app.settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
    MQ_MESSAGE_TTL,
)

from app.models.movie import ElasticRequest
from app.elastic_service.elastic_search import elastic_search

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
    # message = MessageModel(**message_data)  # Восстановление модели Pydantic
    # Обработка сообщения

    message = ElasticRequest(**message_data)
    return elastic_search(message).model_dump()
    # return f"Received message from {message.sender}: {message.text}" # 

