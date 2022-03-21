from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

from db import Base
from .user import User


class Link(Base):
    """Model Link object in database"""
    __tablename__ = "Links"

    id = Column(Integer, primary_key=True, index=True)
    expired = Column(DateTime())
    text = Column(String(), index=True)
    short_text = Column(String(), index=True)
    owner_id = Column(ForeignKey(User.id, ondelete="CASCADE"))
