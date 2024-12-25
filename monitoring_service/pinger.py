from celery import Celery
import psycopg2
from minio import Minio
from minio.error import S3Error
from psycopg2 import OperationalError
from kombu import Queue

from models import PingRequest, PingResponse
from settings import (
    DB_CONFIG,
    MINIO_CONFIG,
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_PING_QUEUE,
    MQ_MESSAGE_TTL,
)

MINIO_TIMEOUT = 1

app = Celery(
    'tasks', 
    broker=f'pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}//', 
    backend='rpc://',
    queue=MQ_ROUTING_KEY_RPC_PING_QUEUE,
)

app.conf.worker_prefetch_multiplier = 1 # Воркер будет брать одну задачу за раз
app.conf.task_queues = (
    Queue(MQ_ROUTING_KEY_RPC_PING_QUEUE, 
    routing_key=MQ_ROUTING_KEY_RPC_PING_QUEUE, 
    queue_arguments=
    {
        'x-message-ttl': MQ_MESSAGE_TTL,
        'x-dead-letter-exchange': 'rpc.dlx', 
        'x-dead-letter-routing-key': 'rpc_dlq'
    }),
)

@app.task(queue=MQ_ROUTING_KEY_RPC_PING_QUEUE, name='ping')
def ping(message_data) -> PingResponse:

    try:
        request = PingRequest(**message_data)

        if request.service_type == "pg":
            connection = psycopg2.connect(
                dbname=DB_CONFIG['dbname'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                host=DB_CONFIG['host'],
                port=DB_CONFIG['port'],
            )
            connection.close()
            return PingResponse(
                service_type=request.service_type,
                pong="pong",
                success=True,
            ).model_dump()
        
        elif request.service_type == "minio":
            minio_client = Minio(
                MINIO_CONFIG['endpoint'],
                access_key=MINIO_CONFIG['access_key'],
                secret_key=MINIO_CONFIG['secret_key'],
                secure=False,  # Установите True, если используете HTTPS
                http_client=Minio.create_http_client(timeout=MINIO_TIMEOUT),
            )
            # Попробуем получить список бакетов для проверки доступности
            buckets = minio_client.list_buckets()
            return PingResponse(
                service_type=request.service_type,
                pong="pong",
                success=True,
            ).model_dump()
    
        else:
            raise ValueError
    except OperationalError as e:
        return PingResponse(
            service_type=request.service_type,
            pong=None,
            success=True,
        ).model_dump()
    except S3Error as e:
        return PingResponse(
            service_type=request.service_type,
            pong=None,
            success=True,
        ).model_dump()
    except Exception as e:
        return PingResponse(
            service_type=request.service_type,
            pong=None,
            success=False,
        ).model_dump()
