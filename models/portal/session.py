"""Session authentication class
"""
from sqlalchemy import Column, ForeignKey, String
from models.base import Base
from models.baseModel import BaseModel


class Session(BaseModel, Base):
    """Session authentication class

    Args:
        BaseModel (BaseModel): baseModel class
        Base (Declarative Base): declarative base
    """    
    __tablename__ = "sessions"
    user_id = Column(
        String(36),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
