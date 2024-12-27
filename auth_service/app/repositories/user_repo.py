from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.connector import *
from app.repositories.models.models import User

class UserRepository:
    def __init__(self):
        pass

    def add_new_user(self, username: str, email: str, password_hash: str, role='viewer') -> int:
        '''
            Function adds new user to a database
            Returns a distinct user_id
        '''

        new_user = User(
            email=email,
            username=username,
            password=password_hash,
            role=role,
            registered_at=datetime.now()
        )

        with get_session() as session:
            session.add(new_user)
            session.flush() # Чтобы получить не None а нормальный user_id до commit

            print(f"User with id {new_user.user_id} has been added to database")
            return new_user.user_id

    def get_user_info(self, login: str) -> User:
        '''
            Returns info about user with given login
        '''

        with get_session() as session:
            user = None
            try:
                user = User.from_orm(session.query(User).filter_by(username == login).one())
                return user
            except NoResultFound:
                print(f"User with login {login} not found in usernames, will try to find in emails")

            try:
                user = User.from_orm(session.query(User).filter_by(email == login).one())
                return user
            except NoResultFound:
                print(f"User with login {login} not found in database")
                return None

    def get_user_id_info(self, user_id: int) -> User:
        '''
            Returns info about user with given user_id
        '''

        with get_session() as session:
            return User.from_orm(session.query(User).filter(User.user_id == user_id).one_or_none())

    def get_user_login_info(self, username: str) -> User:
        '''
            Returns info about user with given username
        '''

        with get_session() as session:
            user_orm = session.query(User).filter(User.username == username).one_or_none()
            if user_orm is None:
                return None
            return User.from_orm(user_orm)

    def get_all_usernames(self) -> list:
        '''
            Returns all registered usernames
        '''
        with get_session() as session:
            usernames = session.query(User.username).all()
            return [name[0] for name in usernames]

    def get_all_emails(self) -> list:
        '''
            Returns all registered emails
        '''
        with get_session() as session:
            emails = session.query(User.email).all()
            return [email[0] for email in emails]