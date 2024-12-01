from passlib.context import CryptContext
from jose import JWTError, jwt
from repositories.user_repo import UserRepository, UserAlreadyExistsError
from datetime import datetime, timedelta
from core.config import settings


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    async def register_user(self, email: str, username: str, password: str):
        hashed_password = self.hash_password(password)
        try:
            await self.user_repository.create_user(email, username, hashed_password)
        except UserAlreadyExistsError as e:
            raise ValueError(f"Registration failed: {str(e)}")
        except Exception as e:
            raise Exception("An unexpected error occurred during registration.")

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, email: str, password: str):
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user