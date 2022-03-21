from datetime import timedelta
from typing import Any

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.user import UserCreate, User, Token
from utils import users as users_utils
from settings import ACCESS_TOKEN_EXPIRE_MINUTES

from .deps import get_db, get_current_active_user
from models.user import User as UserModel


router = APIRouter()


@router.post("/api/sign-up", response_model=User)
def create_user(
        user: UserCreate,
        db: Session = Depends(get_db)
) -> User:
    """Creates users if it not in database"""
    found_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if found_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_add = UserModel(
        username=user.username,
        email=user.email,
        password=users_utils.get_password_hash(user.password)
    )
    db.add(user_add)
    db.commit()
    db.refresh(user_add)
    return user_add


@router.post("/api/token", response_model=Token)
async def login_for_access_token(
        db: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """Creates token for user after successful authentication"""
    user = users_utils.authenticate_user(
        db,
        form_data.username,
        form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = users_utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/api/users/me/")
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """Returns information about current active user """
    return current_user
