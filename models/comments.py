from sqlalchemy import Column, Boolean, Integer, String, ForeignKey
from db.base import Base
from models.mixins import At_Mixin, SoftDelMixin
from sqlalchemy.orm import relationship


class Comments(Base, At_Mixin, SoftDelMixin):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    is_deleted = Column(Boolean, default=False)

    posts = relationship("Posts", back_populates="comments")
    author = relationship("User", back_populates="comments")
