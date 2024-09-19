from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

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

@app.post("/api/login/")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = authenticate_user_by_email(db, user.email, user.password)
    if not user:
        return {"error": "Invalid credentials"}
    return user

