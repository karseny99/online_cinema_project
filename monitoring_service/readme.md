celery flower --broker=pyamqp//guest:guest@localhost:15672//
localhost:5555
celery -A main worker --loglevel=info --prefetch-multiplier=1 --hostname=monitoring_service@%h