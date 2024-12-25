from app.repositories.connector import *
from app.repositories.models.user import User


def get_user_role(user_id: int) -> str:
    '''
        Returns user's role
    '''
    with get_session() as session:
        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        if not user:
            return None
        return User.from_orm(user).role
