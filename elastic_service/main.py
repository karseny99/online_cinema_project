
import asyncio
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

from app.models.models import ElasticRequest
from app.service.elastic_search import elastic_search, elastic_update_index

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


@app.task(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, name='search_movie')
def search_movie(message_data):
    ''' 
        Calls elastic search with given query
        Returns ElasticResponse class
    '''
    message = ElasticRequest(**message_data)
    result = asyncio.run(elastic_search(message))
    return result.model_dump()


@app.task(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, name='update_index')
def update_elastic_index():
    '''
        Updates elastic-index 
    '''
    asyncio.run(elastic_update_index())
