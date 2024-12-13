import time
import pika
from app.models.models import SetMovieRatingRequest, SetMovieRatingResponse
from app.service.movie_rating import MovieRatingService

from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_RPC_QUEUE,
)


def process_request(request_data: SetMovieRatingRequest) -> SetMovieRatingResponse:
    time.sleep(5)
    movie_rating_service = MovieRatingService()
    response = movie_rating_service.new_rating(request_data)
    if not response.success:
        raise ValueError
    return response


def on_request(ch, method, props, body):
    try:
        request_data = body.decode('utf-8')
        print(f"Received message: {request_data}")
        correlation_id = props.correlation_id
        response = process_request(request_data)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=str(response),
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Something went wrong: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def listen_for_request() -> None:
    connection_params = pika.ConnectionParameters(
        host=MQ_HOST,
        port=MQ_PORT,
        credentials=pika.PlainCredentials(RMQ_USER, RMQ_PASSWORD),
    )
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=MQ_ROUTING_KEY_RPC_QUEUE, on_message_callback=on_request)

    print("Waiting for RPC requests...")
    channel.start_consuming()

if __name__ == "__main__":
    listen_for_request()
