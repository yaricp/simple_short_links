from datetime import datetime, timedelta
from typing import Optional

# from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

from models.user import User as UserModel
from settings import (
    SECRET_KEY,
    ALGORITHM
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Gets password hash"""
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    """Authenticate user in system"""
    found_user = db.query(UserModel).filter(
        UserModel.username == username
    ).first()
    if not found_user:
        return False
    if not verify_password(password, found_user.password):
        return False
    return found_user


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):
    """Creates access token for authenticated user"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
