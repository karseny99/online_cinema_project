import os

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
POOL_MAX_SIZE = int(os.getenv("POOL_MAX_SIZE", 20))

# TODO: move to local.env
MQ_HOST = "0.0.0.0"
MQ_PORT = "5672"
RMQ_USER = "guest"
RMQ_PASSWORD = "guest"
MQ_EXCHANGE = ""
MQ_ROUTING_KEY = "movies"
MQ_ROUTING_KEY_DLQ = os.getenv('MQ_ROUTING_KEY_DLQ', 'dlq')
MQ_ROUTING_KEY_RPC_MOVIE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_MOVIE_QUEUE', 'rpc_movie_queue')
MQ_ROUTING_KEY_RPC_USER_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_USER_QUEUE', 'rpc_user_queue')
MQ_ROUTING_KEY_RPC_AUTH_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_AUTH_QUEUE', 'rpc_auth_queue')
MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE', 'rpc_elastic_queue') 
MQ_MESSAGE_TTL = int(os.getenv('MQ_MESSAGE_TTL', 6000))  # Время жизни сообщения в миллисекундах