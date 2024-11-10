from sqlalchemy import select
from sqlalchemy.orm import Session
from models.models import users

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, email: str, username: str, password: str):
        stmt = users.insert().values(email=email, username=username, password=password)
        self.db.execute(stmt)
        self.db.commit()

    def get_user_by_id(self, user_id: int):
        stmt = select(users).where(users.c.id == user_id)
        return self.db.execute(stmt).first()
