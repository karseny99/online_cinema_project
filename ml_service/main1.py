# import pandas as pd
# from sqlalchemy import create_engine
# import time
# from sqlalchemy.future import select

# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from settings import DB_CONFIG, POOL_SIZE, POOL_MAX_SIZE

# DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

# # Создаем синхронный движок для работы с базой данных
# engine = create_engine(
#     url=DATABASE_URL,
#     pool_size=POOL_SIZE,  # Укажите размер пула
#     max_overflow=POOL_MAX_SIZE
# )

# # Создаем фабрику сессий для взаимодействия с базой данных
# SessionLocal = sessionmaker(
#     bind=engine, expire_on_commit=False
# )

# def connection(method):
#     def wrapper(*args, **kwargs):
#         session = SessionLocal()  # Создаем новую сессию
#         try:
#             return method(*args, session=session, **kwargs)
#         except Exception as e:
#             session.rollback()  # Откатываем сессию при ошибке
#             raise e  # Поднимаем исключение дальше
#         finally:
#             session.close()  # Закрываем сессию

#     return wrapper

# from sqlalchemy import Column, Integer, Float, String, Text, TIMESTAMP, ARRAY, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Rating(Base):
#     __tablename__ = 'ratings'
    
#     rating_id = Column(Integer, primary_key=True)  # Уникальный идентификатор рейтинга
#     user_id = Column(Integer)                       # Идентификатор пользователя
#     movie_id = Column(Integer)                      # Идентификатор фильма
#     rating = Column(Float, nullable=False)          # Рейтинг (тип real в PostgreSQL)
#     rated_at = Column(TIMESTAMP, default='CURRENT_TIMESTAMP')  # Время, когда был поставлен рейтинг


# class Movie(Base):
#     __tablename__ = 'movies'
    
#     movie_id = Column(Integer, primary_key=True, autoincrement=True)
#     title = Column(String(256), nullable=False)
#     imdb_id = Column(Integer, nullable=False)

#     @classmethod 
#     def from_orm(cls, movie_orm):
#         return cls(
#             movie_id = movie_orm.movie_id,
#             title = movie_orm.title,
#             imdb_id = movie_orm.imdb_id,
#         )
    
# class Genre(Base):
#     __tablename__ = 'genres'

#     genre_id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(100), nullable=False)

#     @classmethod 
#     def from_orm(cls, genre_orm):
#         return cls(
#             genre_id = genre_orm.genre_id,
#             name = genre_orm.name,
#         )

# class MovieGenre(Base):
#     __tablename__ = 'movie_genre'
    
#     movie_id = Column(Integer, ForeignKey('movies.movie_id'), primary_key=True)
#     genre_id = Column(Integer, ForeignKey('genres.genre_id'), primary_key=True)


# # Запуск таймера

# @connection
# def get_ratings_in_batches(session, batch_size: int) -> None:
#     offset = 0
#     while offset < batch_size * 10:
#         # Выполнение запроса с ограничением и смещением
#         print(f"current: {offset}")
#         query = select(Rating).limit(batch_size).offset(offset)
#         result = session.execute(query)
        
#         # Получение всех строк в текущем батче
#         ratings_list = result.scalars().all()  # Получаем только значения
        
#         # Если батч пустой, выходим из цикла
#         if not ratings_list:
#             break
        
#         # Создание DataFrame из списка объектов Rating
#         df = pd.DataFrame([{
#             'rating_id': rating.rating_id,
#             'user_id': rating.user_id,
#             'movie_id': rating.movie_id,
#             'rating': rating.rating,
#             'rated_at': rating.rated_at
#         } for rating in ratings_list])
        
#         # Сохранение текущего батча в CSV
#         df.to_csv("ratings12.csv", mode='a', header=not bool(offset), index=False)
#         # Увеличение смещения для следующего батча
#         offset += batch_size

# @connection
# def export_movies_to_csv(session, batch_size: int) -> None:
#     offset = 0
#     while True:
#         print(f"Exporting movies, current offset: {offset}")
#         query = select(Movie).limit(batch_size).offset(offset)
#         result = session.execute(query)
        
#         movies_list = result.scalars().all()
        
#         if not movies_list:
#             break
        
#         df = pd.DataFrame([{
#             'movie_id': movie.movie_id,
#             'title': movie.title,
#             'imdb_id': movie.imdb_id
#         } for movie in movies_list])
        
#         df.to_csv("movies.csv", mode='a', header=not bool(offset), index=False)
#         offset += batch_size


# @connection
# def export_genres_to_csv(session, batch_size: int) -> None:
#     offset = 0
#     while True:
#         print(f"Exporting genres, current offset: {offset}")
#         query = select(Genre).limit(batch_size).offset(offset)
#         result = session.execute(query)
        
#         genres_list = result.scalars().all()
        
#         if not genres_list:
#             break
        
#         df = pd.DataFrame([{
#             'genre_id': genre.genre_id,
#             'name': genre.name
#         } for genre in genres_list])
        
#         df.to_csv("genres.csv", mode='a', header=not bool(offset), index=False)
#         offset += batch_size

# @connection
# def export_movie_genres_to_csv(session, batch_size: int) -> None:
#     offset = 0
#     while True:
#         print(f"Exporting movie_genres, current offset: {offset}")
#         query = select(MovieGenre).limit(batch_size).offset(offset)
#         result = session.execute(query)
        
#         movie_genres_list = result.scalars().all()
        
#         if not movie_genres_list:
#             break
        
#         df = pd.DataFrame([{
#             'movie_id': movie_genre.movie_id,
#             'genre_id': movie_genre.genre_id
#         } for movie_genre in movie_genres_list])
        
#         df.to_csv("movie_genres.csv", mode='a', header=not bool(offset), index=False)
#         offset += batch_size



# BATCH_SIZE = 10000
# start_time = time.time()
# print("Starting ...")
# # Выгрузка данных в DataFrame

# get_ratings_in_batches(batch_size=BATCH_SIZE)
# # export_genres_to_csv(batch_size=BATCH_SIZE)
# # export_movie_genres_to_csv(batch_size=BATCH_SIZE)
# # export_movies_to_csv(batch_size=BATCH_SIZE)

# # Остановка таймера
# end_time = time.time()

# # Закрытие подключения
# engine.dispose()

# # Вычисление времени выполнения

# # Сохранение DataFrame в CSV

# execution_time = end_time - start_time
# # Вывод результатов
# print(f"Время выполнения запроса: {execution_time:.2f} секунд")





from app.service.ml import MLRecommendation


cls = MLRecommendation(model_path=None).update_recommendations_from_csv('working.csv')
