from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Schema for data of token in headers"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for other type of token in headers"""
    sub: Optional[str] = None
    exp: Optional[int] = None


class UserCreate(BaseModel):
    """Schema for create a new user"""
    username: str
    email: str
    password: str


class User(BaseModel):
    """Schema for retrieve information about user from database"""
    id: int
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

    class Config:
        orm_mode = True
