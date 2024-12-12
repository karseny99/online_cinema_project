import logging
import time
import json
from typing import TYPE_CHECKING, List, Any
from settings import MQ_EXCHANGE, MQ_ROUTING_KEY
from message_queue.rmq import configure_logging, get_connection
from pika import BasicProperties

from app.models.movie import *
from app.elastic_service.elastic_search import *

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

# logger = logging.getLogger(__name__)

# def produce_message(channel: "BlockingChannel", msg: str) -> None:
#     logger.debug("Send message %s", msg)
#     channel.basic_publish(
#         exchange=MQ_EXCHANGE,
#         routing_key=MQ_ROUTING_KEY,
#         body=msg,
#     )

# def publish_message(data: Any, channel_id: int) -> None:
#     '''
#         Sends results of movie_service into rmq
#         Var data must be a specified pydantic class
#     '''
#     configure_logging()
#     with get_connection() as connection:
#         logger.info("Created connection: %s", connection)
#         with connection.channel(channel_id) as channel:
#             logger.info("New channel created: %s", channel)

#             msg = json.dumps(data)
#             produce_message(channel=channel, msg=msg)
#             logger.info("New message published: %s", msg)

# if __name__ == "__main__":
#     main()
    

def process_request(request_data):
    # Здесь вы можете выполнять сложные задачи
    # if 'contract_type' in request_data and request_data['contract_type'] == 'search_request':
        # search_request = parse_search_request(request_data)
        # response = convert_to_base_contract(elastic_search(search_request))
    response = int(request_data) ** 2
    return response


def on_request(ch, method, props, body) -> None:
    '''
        On request function processes message
    '''
    try:
        request_data = body.decode('utf-8')
        print(f"Received message: {request_data}")
        correlation_id = props.correlation_id
        response = process_request(request_data)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=BasicProperties(correlation_id=correlation_id),
            body=str(response),
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Something went wrong: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag) # Отказ от сообщения в случае ошибки

def listen_for_request() -> None:
    with get_connection() as connection:

        with connection.channel() as channel:
            channel.queue_declare(queue='rpc_queue', durable=True)
            channel.basic_qos(prefetch_count=1)  # Консумер может вытащить из очереди только одно сообщение, как раз про то, что воркер возьмет новое ОДНО сообщение как только освободится
            channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

            print("Waiting for RPC requests...")
            channel.start_consuming()

if __name__ == "__main__":
    listen_for_request()

