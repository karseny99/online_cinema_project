from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.now())
)

movies = Table(
    "movies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("genres", ARRAY(String), nullable=False)
)

tags = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("userID", Integer, ForeignKey("users.id"), nullable=False),
    Column("movieID", Integer, ForeignKey("movies.id"), nullable=False),
    Column("tag", String, nullable=False),
    Column("time", TIMESTAMP, default=datetime.now())
)

rating = Table(
    "rating",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("userID", Integer, ForeignKey("users.id"), nullable=False),
    Column("movieID", Integer, ForeignKey("movies.id"), nullable=False),
    Column("rating", Integer, nullable=False),
    Column("time", TIMESTAMP, default=datetime.now())
)

genome_tags = Table(
    "genome_tags",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tag", String, nullable=False)
)

genome_scores = Table(
    "genome_scores",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("movieID", Integer, ForeignKey("movies.id"), nullable=False),
    Column("tagID", Integer, ForeignKey("tags.id"), nullable=False),
    Column("relevance", Integer, nullable=False),
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
