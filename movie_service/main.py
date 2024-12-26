
import asyncio
from celery import Celery
from pydantic import BaseModel
from kombu import Queue
import json

from app.models.models import MovieRequest, MovieInfoResponse, GenresResponse, RecommendationRequest, RecommendationResponse
from app.services.movie_service import MovieService
from app.services.redis import RedisClient
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
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

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB)


@app.task(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, name='get_movie_info')
def get_movie_info(message_data):
    ''' 
        Calls elastic search with given query
        Returns ElasticResponse class
    '''

    try:
        cache_key = f"get_movie_info:{json.dumps(message_data)}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result
        
        message = MovieRequest(**message_data)

        result = MovieService.get_movie_by_id(message.movie_id)
        redis_client.set(cache_key, result.model_dump(), 600) # 10 minute cache's life
        return result.model_dump()
    except Exception as e:
        print(f"Exception occured: {e}")
        return MovieInfoResponse(movie=None, success=False).model_dump()


@app.task(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, name='get_distinct_genres')
def get_distinct_genres():
    ''' 
        Calls elastic search with given query
        Returns ElasticResponse class
    '''

    try:
        cache_key = f"get_distinct_genres:"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result
       
        result = MovieService.get_distinct_genres()
        redis_client.set(cache_key, result.model_dump(), 24 * 3600) # 24 hours cache's life
        return result.model_dump()
    except Exception as e:
        print(f"Exception occured: {e}")
        return GenresResponse(genres=None, success=False).model_dump()


@app.task(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, name='get_recommendations')
def get_recommendations(message_data):
    ''' 
        Returns list of recommended MovieItems 
    '''

    try:
        cache_key = f"get_recommendations:{json.dumps(message_data)}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result

        message = RecommendationRequest(**message_data)

        result = MovieService.get_recommendations(message)
        redis_client.set(cache_key, result.model_dump(), 24 * 3600) # 24 hours cache's life
        return result.model_dump()
    except Exception as e:
        print(f"Exception occured: {e}")
        return RecommendationResponse(movies=None, success=False).model_dump()

