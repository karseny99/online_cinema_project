import json
import logging
from settings import MQ_ROUTING_KEY_1
from message_queue.rmq import configure_logging, get_connection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

logger = logging.getLogger(__name__)

def process_new_message(ch: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes
):
    msg = json.loads(body)
    logger.info("Received message: %s", msg)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def consume_messages(channel: "BlockingChannel") -> None:
    channel.queue_declare(queue=MQ_ROUTING_KEY_1, durable=True)
    channel.basic_consume(
        queue=MQ_ROUTING_KEY_1,
        on_message_callback=process_new_message,
    )
    logger.warning("Waiting for messages...")
    channel.start_consuming()

def main():
    configure_logging()
    with get_connection() as connection:
        with connection.channel() as channel:
            consume_messages(channel)

if __name__ == "__main__":
    main()
