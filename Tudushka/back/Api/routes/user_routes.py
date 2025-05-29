from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt, JWTError
from back.Api.services.user_service import UserService
from back.Api.models.user_models import UserCreate, UserLogin
import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user_id(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["user_id"]
    except Exception as e:
        raise HTTPException(status_code=401, detail="Не авторизован") from e

@router.post(
    "/register"
)
async def register(user: UserCreate):
    existing = await UserService.get_user_by_email(user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    hashed = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed
    del user_dict["password"]
    user_id = await UserService.create_user(user_dict)
    return {"id": user_id, "email": user.email}

@router.post(
    "/login"
)
async def login(user: UserLogin):
    db_user = await UserService.get_user_by_email(user.email)
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Неверные email или пароль")
    token = create_access_token({"sub": db_user["email"], "user_id": db_user["id"]})
    return {"access_token": token, "token_type": "bearer"}
