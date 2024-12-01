from passlib.context import CryptContext
from jose import JWTError, jwt
from repositories.user_repo import UserRepository
from datetime import datetime, timedelta
from core.config import settings


class RegistrationException(Exception):
    '''Base class for registration exception'''
    pass

class UsernameExistsException(RegistrationException):
    '''Exception thrown when username already exists in db'''
    def __init__(self, message="Username already exists"):
        self.message = message
        super().__init__(self.message)

class EmailExistsException(RegistrationException):
    '''Exception thrown when email already exists in db'''
    def __init__(self, message="Email already exists"):
        self.message = message
        super().__init__(self.message)


class AuthService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def register_user(self, email: str, username: str, password: str, role: str) -> int:
        hashed_password = self.hash_password(password)

        registered_usernames = self.user_repository.get_all_usernames()
        if username in registered_usernames:
            raise UsernameExistsException()

        registered_emails = self.user_repository.get_all_emails()
        if email in registered_emails:
            raise EmailExistsException()

        user_id = self.user_repository.add_new_user(
            username=username,
            email=email,
            password_hash=hashed_password,
            role=role)
        return user_id

    def authenticate_user(self, username: str, password: str):
        user = self.user_repository.get_user_login_info(username)
        if not user:
            return None
        if not self.verify_password(password, user.password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

