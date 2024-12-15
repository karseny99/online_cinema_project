import json
import time
import pika
from app.models.models import SetMovieRatingRequest, SetMovieRatingResponse, BaseContractModel
from app.service.movie_rating import MovieRatingService

from settings import (
    MQ_HOST,
    MQ_PORT,
    RMQ_USER,
    RMQ_PASSWORD,
    MQ_ROUTING_KEY_RPC_USER_QUEUE,
)


def process_request(request_data: SetMovieRatingRequest) -> SetMovieRatingResponse:
    time.sleep(3)
    movie_rating_service = MovieRatingService()
    response = movie_rating_service.new_rating(request_data)
    if not response.success:
        raise ValueError
    return response


def on_request(ch, method, props, body):
    try:
        request_data = json.loads(body.decode('utf-8'))
        print(f"Received message: {request_data}")

        correlation_id = props.correlation_id

        req_model = BaseContractModel(**request_data)
        if req_model.contract_type == "set_rating_request":
            # Преобразуем в модель
            request_model = SetMovieRatingRequest(**req_model.body)
            response_model_body = process_request(request_model)
            response_model = BaseContractModel(
                contract_type="set_rating_response",
                body=response_model_body
            )

            # response_json = json.dumps(response_model.__dict__)
            response_json = response_model.json()

            ch.basic_ack(delivery_tag=method.delivery_tag)
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=correlation_id),
                body=response_json,
            )
        else:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

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
    channel.basic_consume(queue=MQ_ROUTING_KEY_RPC_USER_QUEUE, on_message_callback=on_request)

    print("Waiting for RPC requests...")
    channel.start_consuming()
