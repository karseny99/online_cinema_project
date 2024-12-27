pg_dump --no-owner -Fc -h localhost -p 5432 -U user cinema-db -f dump1112
celery -A main worker --loglevel=info --prefetch-multiplier=1 --hostname=movie_service@%h