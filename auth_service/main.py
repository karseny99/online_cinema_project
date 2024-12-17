from celery import Celery
from kombu import Queue
from app.service.auth_service import EmailExistsException, UsernameExistsException
import json

from app.models.models import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse
from app.service.auth_service import AuthService
from app.service.redis import RedisClient
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_AUTH_QUEUE,
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
    queue=MQ_ROUTING_KEY_RPC_AUTH_QUEUE,
)

app.conf.worker_prefetch_multiplier = 1
app.conf.task_queues = (
    Queue(MQ_ROUTING_KEY_RPC_AUTH_QUEUE,
          routing_key=MQ_ROUTING_KEY_RPC_AUTH_QUEUE,
          queue_arguments=
          {
              'x-message-ttl': MQ_MESSAGE_TTL,
              'x-dead-letter-exchange': 'rpc.dlx',
              'x-dead-letter-routing-key': 'rpc_dlq'
          }),
)

redis_client = RedisClient(REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB)


@app.task(queue=MQ_ROUTING_KEY_RPC_AUTH_QUEUE, name='register_user')
def register_user(message_data):
    '''
        Calls register_user and returns registered user_id
    '''
    auth = AuthService()

    try:
        message = RegisterRequest(**message_data)
        result = auth.register_user(
            username=message.username,
            password=message.password,
            email=message.email,
            role='user'
        )
        # надо обязательно передавать json
        return RegisterResponse(user_id=result, message="registered successfully!").json()
    except UsernameExistsException:
        return RegisterResponse(user_id=-1, message="username already exists").json()
    except EmailExistsException:
        return RegisterResponse(user_id=-1, message="email already exists").json()



@app.task(queue=MQ_ROUTING_KEY_RPC_AUTH_QUEUE, name='login_user')
def login_user(message_data):
    '''
        Calls log-in and returns jwt token
    '''
    auth = AuthService()

    message = LoginRequest(**message_data)
    result = auth.authenticate_user(username=message.username, password=message.password)
    if not result:
        return LoginResponse(
            access_token="",
            token_type="",
            message="user does not exist"
        ).json()

    access_token = auth.create_access_token(data={"sub": result.username})

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        message="token created successfully!"
    ).json()