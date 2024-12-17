from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import DB_CONFIG, POOL_SIZE, POOL_MAX_SIZE

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

# Создаем синхронный движок для работы с базой данных
engine = create_engine(
    url=DATABASE_URL,
    pool_size=POOL_SIZE,  # Укажите размер пула
    max_overflow=POOL_MAX_SIZE
)

# Создаем фабрику сессий для взаимодействия с базой данных
SessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False
)

def connection(method):
    def wrapper(*args, **kwargs):
        session = SessionLocal()  # Создаем новую сессию
        try:
            return method(*args, session=session, **kwargs)
        except Exception as e:
            session.rollback()  # Откатываем сессию при ошибке
            raise e  # Поднимаем исключение дальше
        finally:
            session.close()  # Закрываем сессию

    return wrapper
