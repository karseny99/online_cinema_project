from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int
    email: str
    username: str
