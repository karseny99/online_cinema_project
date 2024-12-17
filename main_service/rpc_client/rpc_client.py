from celery import Celery
from pydantic import BaseModel
from kombu import Exchange, Queue
import random
from settings import (
    RMQ_PASSWORD,
    RMQ_USER,
    MQ_HOST,
    MQ_PORT,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
    MQ_MESSAGE_TTL,
)

class RpcClient:
    def __init__(self, routing_key: str):
        self.routing_key = routing_key
        self.app = Celery('client', 
            broker=f'pyamqp://{RMQ_USER}:{RMQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}//', # Тип брокера (Rabbit в нашем случае)
            backend='rpc://', 
        )

        # настройка для используемой очереди
        self.app.conf.task_queues = (
            Queue(routing_key, routing_key=routing_key, queue_arguments={
                'x-message-ttl': MQ_MESSAGE_TTL,
                'x-dead-letter-exchange': 'rpc.dlx',
                'x-dead-letter-routing-key': 'rpc_dlq'
            }),
        )
        dead_letter_queue_option = {
            'x-message-ttl': MQ_MESSAGE_TTL,
            'x-dead-letter-exchange': 'rpc.dlx',
            'x-dead-letter-routing-key': 'rpc_dlq',
        }

        default_exchange = Exchange(routing_key, type='direct')
        dlx_exchange = Exchange('rpc.dlx', type='direct')

        default_queue = Queue(
            routing_key,
            default_exchange,
            routing_key=routing_key,
            queue_arguments=dead_letter_queue_option
        )
        
        dead_letter_queue = Queue('rpc.dlx', dlx_exchange, routing_key='rpc_dlq')
        self.app.conf.task_queues = (default_queue, dead_letter_queue)

    def send_task(self, function_name: str, request: BaseModel) -> BaseModel:
        '''
            Sends task to movie's service
            Returns Response, None if timed out 
        '''

        # Отправка сообщения через RPC
        result = self.app.send_task(
            function_name, # Название функции в сервисе (tasks - имя файла, process_message - название функции)
            args=[request.model_dump()],
            queue=self.routing_key,    
        )

        # Получение результата
        try:
            response = result.get(timeout=10)  # Ожидание результата до 10 секунд + пришлет именно тому, кто запрашивал, corr_id не нужен
            print('Response:', response)
            return response
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def send_task_no_wait(self, function_name: str, request: BaseModel):
        '''
            Sends task to service without waiting for a response
        '''
        args = [request.model_dump()] if request is not None else []

        # Отправка сообщения через RPC без ожидания результата
        self.app.send_task(
            function_name,
            args=args,
            queue=self.routing_key,
            ignore_result=True,
        )
        print(f'Task {function_name} sent without waiting for a response.')


def get_movie_rpc_client() -> RpcClient:
    '''
        Returns rpc_client for movie's service
    '''
    return RpcClient(MQ_ROUTING_KEY_RPC_MOVIE_QUEUE)


def get_user_rpc_client():
    return 