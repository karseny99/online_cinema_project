from repositories.user_repo import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, email: str, username: str, password: str):
        self.user_repository.create_user(email, username, password)

    def get_user(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)
