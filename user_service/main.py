import logging
from message_queue.rpc_server import listen_for_request

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.info("STARTING user service")
    listen_for_request()
