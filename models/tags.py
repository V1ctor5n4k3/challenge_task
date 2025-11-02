from sqlalchemy import Column, Boolean, Integer, String
from db.base import Base
from models.mixins import At_Mixin, SoftDelMixin
from sqlalchemy.orm import relationship
from models.posts import post_tags


class Tags(Base, At_Mixin, SoftDelMixin):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    posts = relationship("Posts", secondary=post_tags, back_populates="tags")
