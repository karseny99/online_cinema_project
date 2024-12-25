import os

# DB_CONFIG = {
#     "dbname": os.getenv("DB_NAME"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "host": os.getenv("DB_HOST"),
#     "port": os.getenv("DB_PORT"),
# }

# POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
# POOL_MAX_SIZE = int(os.getenv("POOL_MAX_SIZE", 20))

MQ_HOST = os.getenv('MQ_HOST', 'localhost')
MQ_PORT = os.getenv('MQ_PORT', '5672')
RMQ_USER = os.getenv('RMQ_PASSWORD', 'guest')
RMQ_PASSWORD = os.getenv('RMQ_PASSWORD', 'guest')
MQ_EXCHANGE = os.getenv('MQ_EXCHANGE', '')
MQ_ROUTING_KEY_DLQ = os.getenv('MQ_ROUTING_KEY_DLQ', 'dlq')
MQ_ROUTING_KEY_RPC_MOVIE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_MOVIE_QUEUE', 'rpc_movie_queue')
MQ_ROUTING_KEY_RPC_USER_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_USER_QUEUE', 'rpc_user_queue')
MQ_ROUTING_KEY_RPC_AUTH_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_AUTH_QUEUE', 'rpc_auth_queue')
MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_ELASTIC_QUEUE', 'rpc_elastic_queue') 
MQ_ROUTING_KEY_RPC_PING_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_PING_QUEUE', 'rpc_ping_queue') 
MQ_MESSAGE_TTL = int(os.getenv('MQ_MESSAGE_TTL', 6000))  # Время жизни сообщения в миллисекундах