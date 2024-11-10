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

