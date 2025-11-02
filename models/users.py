from sqlalchemy import Column, Integer, String, Boolean
from db.base import Base
from models.mixins import At_Mixin, SoftDelMixin
from sqlalchemy.orm import relationship


class User(Base, At_Mixin, SoftDelMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    posts = relationship("Posts", back_populates="owner")
    comments = relationship("Comments", back_populates="author")
