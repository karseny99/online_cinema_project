from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.models import users

class UserAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"User with email {email} already exists."
        super().__init__(self.message)

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, email: str, username: str, password: str):
        stmt_exist = select(users).where(users.c.email == email)
        result = await self.db.execute(stmt_exist)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise UserAlreadyExistsError(email)

        stmt = users.insert().values(email=email, username=username, password=password)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_user_by_email(self, user_email: str):
        stmt = select(users).where(users.c.email == user_email)
        result = await self.db.execute(stmt)
        return result.first()
