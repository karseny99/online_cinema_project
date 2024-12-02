# from sqlalchemy import Column, Integer, String, DateTime, Text
# from sqlalchemy.ext.declarative import declarative_base
#
# Base = declarative_base()
#
# class Movie(Base):
#     __tablename__ = 'movies'
#
#     movie_id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String(256), nullable=False)
#     published_year = Column(Integer, nullable=True)
#     isbn = Column(String(256), unique=True, nullable=True)
#     description = Column(Text, nullable=True)
#     added_at = Column(DateTime, nullable=False)
#     file_path = Column(String(512), nullable=False)
#     cover_image_path = Column(String(512), nullable=True)
#
#     @classmethod
#     def from_orm(cls, movie_orm):
#         return cls(
#             book_id=movie_orm.movie_id,
#             title=movie_orm.title,
#             published_year=movie_orm.published_year,
#             isbn=movie_orm.isbn,
#             description=movie_orm.description,
#             added_at=movie_orm.added_at,
#             file_path=movie_orm.file_path,
#             cover_image_path=movie_orm.cover_image_path
#         )