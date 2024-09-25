from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str
    password: str

class UserCreate(UserBase):
    username: str

class User(UserCreate):
    id: int

    class Config:
        from_attributes = True
