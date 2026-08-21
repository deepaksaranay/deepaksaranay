from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from .auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])

_USERS: dict[str, str] = {}


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    if user.username in _USERS:
        raise HTTPException(status_code=409, detail="Username already registered")
    _USERS[user.username] = hash_password(user.password)
    return {"message": "User registered successfully"}


@router.post("/login", response_model=Token)
def login(user: UserCreate):
    password_hash = _USERS.get(user.username)
    if not password_hash or not verify_password(user.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_access_token(user.username), "token_type": "bearer"}
