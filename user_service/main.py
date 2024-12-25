from pyexpat.errors import messages

from celery import Celery
from kombu import Queue
import json
import logging

from app.models.models import SetMovieRatingRequest, SetMovieRatingResponse, GetMovieRatingRequest, GetMovieRatingResponse, UserInfoRequest, UserInfoResponse
from app.service.movie_rating import MovieRatingService
from app.service.user import get_user_info
from app.service.redis import RedisClient
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_MESSAGE_TTL,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_PASSWORD,
    REDIS_DB,
    MQ_ROUTING_KEY_RPC_USER_QUEUE,
)

log = logging.getLogger(__name__)

app = Celery(
    'tasks',
    broker=f'pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}//',
    backend='rpc://',
    queue=MQ_ROUTING_KEY_RPC_USER_QUEUE,
)

app.conf.worker_prefetch_multiplier = 1
app.conf.task_queues = (
    Queue(MQ_ROUTING_KEY_RPC_USER_QUEUE,
          routing_key=MQ_ROUTING_KEY_RPC_USER_QUEUE,
          queue_arguments=
          {
              'x-message-ttl': MQ_MESSAGE_TTL,
              'x-dead-letter-exchange': 'rpc.dlx',
              'x-dead-letter-routing-key': 'rpc_dlq'
          }),
)

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB)


@app.task(queue=MQ_ROUTING_KEY_RPC_USER_QUEUE, name="set_movie_rating")
def set_movie_rating(message_data):
    '''
        Calls set_rating and returns movie_id, user_id, message
    '''
    message = SetMovieRatingRequest(**message_data)

    rating_service = MovieRatingService()
    res = rating_service.new_rating(req=message)

    res.movie_id = message.movie_id
    res.user_id = message.user_id
    if res.success:
        res.message = "rating set successfully!"

    cache_key = f"get_movie_rating:{json.dumps({'movie_id': message.movie_id, 'user_id': message.user_id}, sort_keys=True)}"

    cached_result = redis_client.get(cache_key)
    if cached_result:
        cache_update = GetMovieRatingResponse(movie_id=res.movie_id, user_id=res.user_id, rating=int(message.rating), success=True)
        redis_client.set(cache_key, cache_update.model_dump(), 24 * 3600)  # Обновляем кэш с новым рейтингом

    return SetMovieRatingResponse(
        movie_id=message.movie_id,
        user_id=message.user_id,
        success=res.success,
        message=res.message
    ).json()


@app.task(queue=MQ_ROUTING_KEY_RPC_USER_QUEUE, name="get_movie_rating")
def get_movie_rating(message_data):
    '''
        Returns user's score on given movie
    '''
    try:
        cache_key = f"get_movie_rating:{json.dumps(message_data)}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result

        message = GetMovieRatingRequest(**message_data) 

        rating_service = MovieRatingService()
        result = rating_service.get_rating(req=message)
        redis_client.set(cache_key, result.model_dump(), 24 * 3600)
        print(result.model_dump())
        return result.model_dump()
    except Exception as e:
        log.error(f"Error occured: {str(e)}")
        return GetMovieRatingResponse(movie_id=None, user_id=None, rating=None, success=False).model_dump()


@app.task(queue=MQ_ROUTING_KEY_RPC_USER_QUEUE, name="get_user_info")
def get_info(message_data):
    '''
        Returns user's info w/ password
    '''
    try:
        cache_key = f"get_user_info:{json.dumps(message_data)}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result

        request = UserInfoRequest(**message_data) 

        result = get_user_info(request)
        redis_client.set(cache_key, result.model_dump(), 24 * 3600)
        return result.model_dump()
    except Exception as e:
        log.error(f"Error occured: {str(e)}")
        return GetMovieRatingResponse(movie_id=None, user_id=None, rating=None, success=False).model_dump()