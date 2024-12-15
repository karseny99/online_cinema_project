FROM rabbitmq:3-management

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y python3 python3-venv python3-pip

# Создаем виртуальное окружение
RUN python3 -m venv /venv

# Активируем виртуальное окружение и устанавливаем pika
RUN /venv/bin/pip install pika

# Копируем скрипт и делаем его исполняемым
COPY init_queue.py /init_queue.py
COPY settings.py /settings.py
RUN chmod +x /init_queue.py

# Запускаем RabbitMQ и инициализируем очереди
CMD ["sh", "-c", "rabbitmq-server & sleep 10 && /venv/bin/python /init_queue.py && wait"]
