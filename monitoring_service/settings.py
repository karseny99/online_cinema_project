import os

# PostgreSQL
DB_CONFIG = {
    "dbname": "cinema-db",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": "5432",
}
# DB_CONFIG = {
#     "dbname": os.getenv("DB_NAME"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "host": os.getenv("DB_HOST"),
#     "port": os.getenv("DB_PORT"),
# }

MINIO_CONFIG = {
    'endpoint': 'minio_host:9000',
    'access_key': 'your_access_key',
    'secret_key': 'your_secret_key',
}


POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
POOL_MAX_SIZE = int(os.getenv("POOL_MAX_SIZE", 20))

# RabbitMQ
MQ_HOST = os.getenv('MQ_HOST', 'localhost')
MQ_PORT = os.getenv('MQ_PORT', '5672')
RMQ_USER = os.getenv('RMQ_PASSWORD', 'guest')
RMQ_PASSWORD = os.getenv('RMQ_PASSWORD', 'guest')
MQ_EXCHANGE = os.getenv('MQ_EXCHANGE', '')
MQ_ROUTING_KEY_DLQ = os.getenv('MQ_ROUTING_KEY_DLQ', 'dlq')
MQ_MESSAGE_TTL = int(os.getenv('MQ_MESSAGE_TTL', 6000))  # Время жизни сообщения в миллисекундах
MQ_ROUTING_KEY_RPC_PING_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_PING_QUEUE', 'rpc_ping_queue') 

# Redis
REDIS_HOST = os.getenv('RS_HOST', 'localhost')
REDIS_PORT = os.getenv('RS_POST', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_DB = os.getenv('RS_DB', '0') # В редисе можно создать разные бдшки, я для сервисов буду работать с разными бдшками в редисе. Это "ид" бдшки