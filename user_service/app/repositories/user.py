from app.repositories.connector import *
from app.repositories.models.user import User


def get_user_info(user_id: int) -> User:
    '''
        Returns user's info
    '''
    with get_session() as session:
        user = session.query(User).filter(User.user_id == user_id).one_or_none()
        if not user:
            return None

        result = User.from_orm(user)
        result.password = None
        return result
