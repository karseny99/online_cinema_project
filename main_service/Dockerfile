FROM rabbitmq:3-management

RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

RUN python3 -m venv venv && \
    /venv/bin/pip install pika

COPY message_queue/init_queue.py /init_queue.py
COPY settings.py /settings.py
RUN chmod +x /init_queue.py

CMD ["sh", "-c", "rabbitmq-server & sleep 10 && /venv/bin/python3 /init_queue.py && wait"]