from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database.db import get_db
from models.user import User as UserModel
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token,
)

router = APIRouter()
security = HTTPBearer()


class User(BaseModel):
    email: str
    password: str
    role: str = "user"


@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    existing = db.query(UserModel).filter(UserModel.email == user.email).first()

    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    new_user = UserModel(
        email=user.email,
        password=hash_password(user.password),
        role=user.role,
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered"}


@router.post("/login")
def login(user: User, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_access_token({
        "email": db_user.email,
        "role": db_user.role,
    })

    return {"access_token": token}


@router.get("/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
