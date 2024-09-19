from datetime import datetime, timedelta, timezone

import jwt

from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from schemas import UserModify, User
from crud import get_user_by_email

SECRET_KEY = "cd9c6fab65ca7e507153d7246ccc8219ba2b42d659ed9b1687d9b9697d53805c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    user_id: int

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user_by_email(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return create_access_token(data={"sub": user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)

def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
