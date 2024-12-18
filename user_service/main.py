from pyexpat.errors import messages

from celery import Celery
from kombu import Queue
import json

from app.models.models import SetMovieRatingRequest, SetMovieRatingResponse
from app.service.movie_rating import MovieRatingService
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
    return SetMovieRatingResponse(
        movie_id=message.movie_id,
        user_id=message.user_id,
        success=res.success,
        message=res.message
    ).json()
