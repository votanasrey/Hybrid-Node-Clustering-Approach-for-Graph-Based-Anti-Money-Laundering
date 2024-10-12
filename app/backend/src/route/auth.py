from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.core.connection import get_db
from src.model.user import User
from src.service.hash import Hash
from src.service.token_service import sign_jwt

router = APIRouter()


class UserRegisterDTO(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone_number: str


@router.post('/register')
async def register(data: UserRegisterDTO, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=data.username,
        email=data.email,
        password=Hash.bcrypt(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        phone_number=data.phone_number,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return sign_jwt(new_user.id)


class UserLoginDTO(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(data: UserLoginDTO, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == data.username) | (User.email == data.username)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not Hash.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return sign_jwt(user.id)
