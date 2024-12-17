from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from settings import DB_CONFIG, POOL_SIZE, POOL_MAX_SIZE

DATABASE_URL = f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

# Создаем асинхронный движок для работы с базой данных
engine = create_async_engine(
    url=DATABASE_URL,
    pool_size=POOL_SIZE,  # Укажите размер пула
    max_overflow=POOL_MAX_SIZE
)
# Создаем фабрику сессий для взаимодействия с базой данных
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                # Явно не открываем транзакции, так как они уже есть в контексте
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()  # Откатываем сессию при ошибке
                raise e  # Поднимаем исключение дальше

    return wrapper