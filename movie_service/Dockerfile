FROM rabbitmq:3-management

RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install pika

# Копируем скрипт и делаем его исполняемым
COPY message_queue/init_queue.py /init_queue.py
COPY settings.py /settings.py
RUN chmod +x /init_queue.py

# Запускаем RabbitMQ и инициализируем очереди
CMD ["sh", "-c", "rabbitmq-server & sleep 10 && python3 /init_queue.py && wait"]
