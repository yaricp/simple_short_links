from datetime import datetime
from pydantic import BaseModel, AnyUrl


class LinkIn(BaseModel):
    """Schema for create a new link"""
    text: AnyUrl


class LinkUpdate(BaseModel):
    """Schema for update link"""
    short_text: str
    expired: datetime


class Link(BaseModel):
    """Schema for retrieve information about link from database"""
    id: int
    text: str
    short_text: str
    expired: datetime
    owner_id: int

    class Config:
        orm_mode = True
