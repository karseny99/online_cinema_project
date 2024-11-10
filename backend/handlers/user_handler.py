from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.user_service import UserService
from dto.user_dto import UserDTO
from repositories.user_repo import UserRepository

router = APIRouter()

def get_db():
    from main import db
    return db()

@router.post("/users/", response_model=UserDTO)
def create_user(email: str, username: str, password: str, db: Session = Depends(get_db)):
    user_use_case = UserService(UserRepository(db))
    user_use_case.create_user(email, username, password)

@router.get("/users/{user_id}", response_model=UserDTO)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_use_case = UserService(UserRepository(db))
    user = user_use_case.get_user(user_id)
    return UserDTO(id=user.id, email=user.email, username=user.username)  

