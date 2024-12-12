# import os

# DB_CONFIG = {
#     "dbname": os.getenv("DB_NAME"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD"),
#     "host": os.getenv("DB_HOST"),
#     "port": os.getenv("DB_PORT"),
# }

# POOL_SIZE = int(os.getenv("POOL_SIZE", 10))
# POOL_MAX_SIZE = int(os.getenv("POOL_MAX_SIZE", 20))

# TODO: move to local.env
MQ_HOST = "0.0.0.0"
MQ_PORT = "5672"
RMQ_USER = "guest"
RMQ_PASSWORD = "guest"
MQ_EXCHANGE = ""
MQ_ROUTING_KEY = "movies"