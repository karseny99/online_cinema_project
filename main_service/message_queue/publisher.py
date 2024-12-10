import logging
import time
from time import sleep
from typing import TYPE_CHECKING
from settings import MQ_EXCHANGE, MQ_ROUTING_KEY
from rmq import configure_logging, get_connection

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

logger = logging.getLogger(__name__)

def produce_message(channel: "BlockingChannel", msg: str) -> None:
    # queue = channel.queue_declare(queue=MQ_ROUTING_KEY)
    logger.debug("Send message %s", msg)
    channel.basic_publish(
        exchange=MQ_EXCHANGE,
        routing_key=MQ_ROUTING_KEY,
        body=msg,
    )


def main():
    configure_logging()
    with get_connection() as connection:
        logger.info("Created connection: %s", connection)
        with connection.channel() as channel:
            logger.info("New channel created: %s", channel)

            for i in range(1, 10):
                msg = f"Hello! I'm message{i}!"
                produce_message(channel=channel, msg=msg)
                logger.info("New message published: %s", msg)
                time.sleep(1)

if __name__ == "__main__":
    main()