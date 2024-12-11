import logging
import time
from typing import TYPE_CHECKING
from settings import MQ_EXCHANGE, MQ_ROUTING_KEY
from rmq import get_connection, configure_logging

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

logger = logging.getLogger(__name__)

def process_new_message(
        ch: "BlockingChannel",
        method: "Basic.Deliver",
        properties: "BasicProperties",
        body: bytes
):
    logger.debug("ch: %s", ch)
    logger.debug("method: %s", method)
    logger.debug("properties: %s", properties)
    logger.debug("body: %s", body)

    logger.warning("[ ] Start processing message (expensive task!) %r", body)
    start_time = time.time()
    ...
    time.sleep(1)
    ...
    end_time = time.time()
    logger.info("Finished processing message %r, sending ack!", body)
    ch.basic_ack(delivery_tag=method.delivery_tag) # подтверждаем, что сообщение доставлено, чтобы оно больше не отправлялось в очередь
    logger.warning(
        "[X] Finished in %.2fs processing message %r",
        end_time - start_time,
        body,
    )

def consume_messages(channel: "BlockingChannel") -> None:
    channel.basic_consume(
        queue=MQ_ROUTING_KEY,
        on_message_callback=process_new_message,
        # auto_ack=True, # по сути флажок автоматического подтверждения того, что сообщение получено(так для каждого msg)
        # если не делать его True, сообщение будет еще раз добавлено в очередь
        # не очень безопасный способ
    )
    logger.warning("Waiting for messages...")
    channel.start_consuming() # начинаем ждать сообщения


def main():
    configure_logging()
    with get_connection() as connection:
        logger.info("Created connection: %s", connection)
        with connection.channel() as channel:
            logger.info("New channel created: %s", channel)

            consume_messages(channel=channel)

if __name__ == "__main__":
    main()