from sqlalchemy import Column, Integer, String, Boolean

from db import Base


class User(Base):
    """Model User object in database"""
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(), index=True)
    email = Column(String())
    password = Column(String())
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)
