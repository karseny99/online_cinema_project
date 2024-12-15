import logging
import time
import json
from typing import TYPE_CHECKING, List, Any
from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_RPC_MOVIE_QUEUE,
)

# from message_queue.rmq import configure_logging, get_connection
import pika

from app.models.movie import *
from app.elastic_service.elastic_search import *

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

def process_request(request_data: str) -> BaseContractModel:

    '''
        Parses given message and calls for function depends on contract_type
        Returns base contract message  
    '''
    try:
        result = None
        request = BaseContractModel.parse_raw(request_data)

        if request.contract_type == "search_request":
            result: BaseContractModel = convert_to_base_contract(elastic_search(parse_search_request(request)))

        return result
    except:
        raise ValueError()


def on_request(ch, method, props, body):
    try:
        request_data = body.decode('utf-8')
        print(f"Received message: {request_data}")
        correlation_id = props.correlation_id
        response = process_request(request_data)
        response_body = response.json()
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=response_body,
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Something went wrong: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)  # Отказ от сообщения в случае ошибки

def listen_for_request() -> None:
    connection_params = pika.ConnectionParameters(
        host=MQ_HOST,  # Убедитесь, что это имя сервиса в docker-compose
        port=MQ_PORT,
        credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),  # Используйте ваши учетные данные
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MQ_ROUTING_KEY_RPC_MOVIE_QUEUE, on_message_callback=on_request)

    print("Waiting for RPC requests...")
    channel.start_consuming()

if __name__ == "__main__":
    listen_for_request()

