import os

MQ_HOST = os.getenv('MQ_HOST', 'localhost')
MQ_PORT = os.getenv('MQ_PORT', '5672')
RMQ_USER = os.getenv('RMQ_PASSWORD', 'guest')
RMQ_PASSWORD = os.getenv('RMQ_PASSWORD', 'guest')
MQ_EXCHANGE = os.getenv('MQ_EXCHANGE', '')
MQ_ROUTING_KEY_DLQ = os.getenv('MQ_ROUTING_KEY_DLQ', 'dlq')
MQ_ROUTING_KEY_RPC_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_QUEUE', 'rpc_user_service_queue')
MQ_ROUTING_KEY_RPC_RESPONSE_QUEUE = os.getenv('MQ_ROUTING_KEY_RPC_RESPONSE_QUEUE', 'rpc_user_service_response_queue')
MQ_MESSAGE_TTL = int(os.getenv('MQ_MESSAGE_TTL', 6000))  # Время жизни сообщения в миллисекундах