
from celery import Celery
from kombu import Queue
import json

from app.models.models import ElasticRequest
from app.services.elastic_search import elastic_search, elastic_update_index
from app.services.redis import RedisClient
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE,
    MQ_MESSAGE_TTL,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_DB,
)

app = Celery(
    'tasks', 
    broker=f'pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}//', 
    backend='rpc://',
    queue=MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE,
)

app.conf.worker_prefetch_multiplier = 1 # Воркер будет брать одну задачу за раз
app.conf.task_queues = (
    Queue(MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE, 
    routing_key=MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE, 
    queue_arguments=
    {
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': 'rpc.dlx', 
        'x-dead-letter-routing-key': 'rpc_dlq'
    }),
)

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB)


@app.task(queue=MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE, name='search_movie')
def search_movie(message_data) -> dict:
    ''' 
        Calls elastic search with given query
        Returns ElasticResponse class
    '''

    cache_key = f"search_movie:{json.dumps(message_data)}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return cached_result
    
    message = ElasticRequest(**message_data)
    result = elastic_search(message)

    redis_client.set(cache_key, result.model_dump(), 600) # 10 minute cache's life
    return result.model_dump()


@app.task(queue=MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE, name='update_index')
def update_elastic_index() -> None:
    '''
        Updates elastic-index 
    '''
    elastic_update_index()
