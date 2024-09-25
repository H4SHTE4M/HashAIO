from fastapi import FastAPI, Depends, Response, Cookie
from sqlalchemy.orm import Session
from typing import Annotated

from db import crud, models, schemas
from db.database import SessionLocal, engine
from db.auth import authenticate_user_by_email

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/login")
def login(user: schemas.UserBase, db: Session = Depends(get_db), response: Response = None):
    flag, token = authenticate_user_by_email(db, user.email, user.password)
    if not flag:
        return {"error": "Invalid credentials"}
    response.set_cookie(key="token", value=token)
    return {"user": user.email, "token": token}

@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    success, user = crud.create_user(db, user)
    if not success:
        return {"success", "failed"}
    return {"username": user.username, "success": "success"}

@app.get("/users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: Annotated[str | None, Cookie()] = None):
    if token is None:
        return {"error": "Invalid token             "}
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

    