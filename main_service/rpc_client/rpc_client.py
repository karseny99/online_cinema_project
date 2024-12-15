from pyexpat.errors import messages

import pika
import uuid
import json
import time
from models.models import BaseContractModel
from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
    MQ_ROUTING_KEY_RPC_MOVIE_RESPONSE_QUEUE,
    MQ_ROUTING_KEY_RPC_USER_QUEUE,
    MQ_ROUTING_KEY_RPC_USER_RESPONSE_QUEUE,
)

class RpcClient:
    def __init__(self, request_queue: str, response_queue: str):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=MQ_HOST,
            port=MQ_PORT,
            credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
        ))
        self.request_queue = request_queue
        self.response_queue = response_queue

        self.channel = self.connection.channel()
        self.callback_queue = self.response_queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=False,
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        # print(f"Received response: {body} with correlation_id: {props.correlation_id}")

        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def call(self, contract_message: BaseContractModel) -> BaseContractModel:
        self.response = None
        self.corr_id = str(uuid.uuid4())
        # print(f"Sending request with correlation_id: {self.corr_id}")

        message_body = contract_message.json()
        # message_body = json.dumps(contract_message.__dict__)

        self.channel.basic_publish(
            exchange='',
            routing_key=self.request_queue,  # Используем глобальный ключ маршрутизации
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message_body
        )

        # Ожидаем ответ
        timeout = time.time() + 7
        while self.response is None:
            # Проверяем, не истекло ли время ожидания
            if time.time() > timeout:
                print(" [!] No response received, moving to the next request.")
                break  # Выходим из цикла, если время ожидания истекло
            self.connection.process_data_events(time_limit=10)  # Обрабатываем события
        
        if self.response is not None:
            self.response = BaseContractModel(**json.loads(self.response.decode('utf-8')))
            # print(self.response)
            
        return self.response
    


def get_movie_rpc_client() -> RpcClient:
    '''
        Returns configured movie rpc client
    '''
    return RpcClient(MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, MQ_ROUTING_KEY_RPC_MOVIE_RESPONSE_QUEUE)

def get_user_rpc_client() -> RpcClient:
    '''
        Returns configured user rpc client
    '''
    return RpcClient(MQ_ROUTING_KEY_RPC_USER_QUEUE, MQ_ROUTING_KEY_RPC_USER_RESPONSE_QUEUE)