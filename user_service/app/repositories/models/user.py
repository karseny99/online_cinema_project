from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(50), nullable=True)
    email = Column(String(100), nullable=True)
    password = Column(String(256), nullable=True)
    role = Column(String(10), nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=True)

    @classmethod
    def from_orm(cls, user_orm):
        return cls(
            user_id = user_orm.user_id,
            username = user_orm.username,
            email = user_orm.email,
            role = user_orm.role,
            registered_at=user_orm.registered_at
        )