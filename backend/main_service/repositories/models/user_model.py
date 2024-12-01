from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(String(10), default='reader', nullable=False)
    register_at = Column(DateTime, default=datetime.now())

    @classmethod
    def from_orm(cls, user_orm):
        return cls(
            user_id = user_orm.user_id,
            email = user_orm.email,
            username = user_orm.username,
            password = user_orm.password,
            role = user_orm.role,
            register_at = user_orm.register_at
        )