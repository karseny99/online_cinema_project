from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from settings import DB_CONFIG, POOL_SIZE, POOL_MAX_SIZE

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

engine = create_engine(
    url=DATABASE_URL,
    pool_size=POOL_SIZE,  
    max_overflow=POOL_MAX_SIZE
)

SessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False
)

def connection(method):
    def wrapper(*args, **kwargs):
        session = SessionLocal() 
        try:
            return method(*args, session=session, **kwargs)
        except Exception as e:
            session.rollback() 
            raise e  
        finally:
            session.close()  

    return wrapper
