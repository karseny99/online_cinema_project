import json
import logging
from time import sleep
from settings import MQ_EXCHANGE, MQ_ROUTING_KEY_2
from message_queue.rmq import configure_logging, get_connection
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

logger = logging.getLogger(__name__)

def produce_message(channel: "BlockingChannel", msg: str) -> None:
    body = json.dumps(msg)
    logger.debug("Send message: %s", body)
    channel.basic_publish(
        exchange=MQ_EXCHANGE,
        routing_key=MQ_ROUTING_KEY_2,
        body=body,
    )

def main():
    configure_logging()
    with get_connection() as connection:
        logger.info("Created connection: %s", connection)
        with connection.channel() as channel:
            for i in range(1, 10):
                msg = {"id": i, "content": f"Message {i} from Service 2"}
                produce_message(channel, msg)
                logger.info("New message published: %s", msg)
                sleep(4)

if __name__ == "__main__":
    main()
