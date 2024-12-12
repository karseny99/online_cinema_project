import logging
import time
import json
from app.models.movie_item import MovieItem
from typing import TYPE_CHECKING, List, Any
from settings import MQ_EXCHANGE, MQ_ROUTING_KEY
from rmq import configure_logging, get_connection

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel

logger = logging.getLogger(__name__)

def produce_message(channel: "BlockingChannel", msg: str) -> None:
    logger.debug("Send message %s", msg)
    channel.basic_publish(
        exchange=MQ_EXCHANGE,
        routing_key=MQ_ROUTING_KEY,
        body=msg,
    )

def publish_message(data: Any) -> None:
    '''
        Sends results of movie_service into rmq
        Var data must be a specified pydantic class
    '''
    configure_logging()
    with get_connection() as connection:
        logger.info("Created connection: %s", connection)
        with connection.channel() as channel:
            logger.info("New channel created: %s", channel)

            msg = json.dumps(data)
            produce_message(channel=channel, msg=msg)
            logger.info("New message published: %s", msg)

if __name__ == "__main__":
    main()