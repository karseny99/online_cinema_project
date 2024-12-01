tmp for fun
```bash
uvicorn main:app --reload
```

migrations generate
```bash
alembic revision --autogenerate -m "Create tables"
```
migration up
```bash
alembic upgrade head
```

s3 up
```bash
docker-compose up 
```

```bash
root@098f18c7ed31:/# psql -U user -d cinema-db
```

```bash
docker run -d --name cinema-db-container -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=cinema-db -p 5432:5432 postgres:16.6-alpine3.19
```