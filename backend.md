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
root@098f18c7ed31:/# psql -U pg-user -d cinema-db
```