from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import jwt, JWTError
from back.Api.services.user_service import UserService, authenticate_user
from back.Api.models.user_models import UserCreate, UserLogin
from back.settings import SECRET_KEY, ALGORITHM
from back.security import hash_password, verify_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # путь, где выдают токен

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

@router.post(
    "/register"
)
async def register(user: UserCreate):
    existing = await UserService.get_user_by_email(user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    hashed = hash_password(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed
    del user_dict["password"]
    user_id = await UserService.create_user(user_dict)
    return {"id": user_id, "email": user.username}

@router.post(
    "/login"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token({"user_id": user["id"]})
    return {"access_token": token, "token_type": "bearer"}
