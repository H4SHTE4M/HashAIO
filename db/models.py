import permissions

from sqlalchemy import Boolean, Column, Integer, String
from database import Base



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    permission = Column(Integer, default=permissions.USER)
    is_active = Column(Boolean, default=True)
