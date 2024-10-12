from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.core.connection import get_db
from src.model.user import User
from src.service.hash import Hash
from src.service.jwt_bearer import JWTBearer
from src.service.token_service import sign_jwt, decode_jwt
from src.util.response import success_response, error_response

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
        return error_response(message="Username already registered", status_code=HTTPStatus.CONFLICT)

    if db.query(User).filter(User.email == data.email).first():
        return error_response(message="Email already registered", status_code=HTTPStatus.CONFLICT)

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
    token = sign_jwt(new_user.id)
    return success_response("User has been register successfully", token, status_code=HTTPStatus.CREATED)


class UserLoginDTO(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(data: UserLoginDTO, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == data.username) | (User.email == data.username)).first()
    if not user:
        return error_response(message="Invalid credentials", status_code=HTTPStatus.NOT_FOUND)

    if not Hash.verify(data.password, user.password):
        return error_response(message="Invalid password", status_code=HTTPStatus.NOT_FOUND)

    token = sign_jwt(user.id)
    return success_response("User has been login successfully", token)


@router.get('/me', dependencies=[Depends(JWTBearer())])
async def get_user_info(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization").split(" ")[1]
    decoded_token = decode_jwt(token)

    if decoded_token is None:
        return error_response(message="Invalid or expired token.", status_code=HTTPStatus.FORBIDDEN)

    user_id = decoded_token.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return error_response(message="User not found", status_code=HTTPStatus.NOT_FOUND)

    return success_response("User info retrieved successfully", {
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar
    })
