import os

MQ_HOST = os.getenv('MQ_HOST', 'localhost')
MQ_PORT = os.getenv('MQ_PORT', '5672')
RMQ_USER = os.getenv('RMQ_PASSWORD', 'guest')
RMQ_PASSWORD = os.getenv('RMQ_PASSWORD', 'guest')
MQ_EXCHANGE = os.getenv('MQ_EXCHANGE', '')
MQ_ROUTING_KEY_DLQ = os.getenv('MQ_ROUTING_KEY_DLQ', 'dlq')
MQ_ROUTING_KEY_RPC_MOVIE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_MOVIE_QUEUE', 'rpc_movie_queue')
MQ_ROUTING_KEY_RPC_MOVIE_RESPONSE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_MOVIE_RESPONSE_QUEUE', 'rpc_movie_response_queue')
MQ_ROUTING_KEY_RPC_USER_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_USER_QUEUE', 'rpc_user_queue')
MQ_ROUTING_KEY_RPC_USER_RESPONSE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_USER_RESPONSE_QUEUE', 'rpc_user_response_queue')
MQ_ROUTING_KEY_RPC_AUTH_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_AUTH_QUEUE', 'rpc_auth_queue')
MQ_ROUTING_KEY_RPC_AUTH_RESPONSE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_AUTH_RESPONSE_QUEUE', 'rpc_auth_response_queue')
MQ_MESSAGE_TTL = int(os.getenv('MQ_MESSAGE_TTL', 6000))  # Время жизни сообщения в миллисекундах

REDIS_HOST = os.getenv('RS_HOST', 'localhost')
REDIS_PORT = os.getenv('RS_POST', '6379')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
REDIS_DB = os.getenv('RS_DB', '3') # В редисе можно создать разные бдшки, я для сервисов буду работать с разными бдшками в редисе. Это "ид" бдшки
