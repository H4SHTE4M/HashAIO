from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    permission: int

class UserModify(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
