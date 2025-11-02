from sqlalchemy import Column, Boolean, Integer
from sqlalchemy import String, Text, ForeignKey, Table
from db.base import Base
from models.mixins import At_Mixin, SoftDelMixin
from sqlalchemy.orm import relationship

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Posts(Base, At_Mixin, SoftDelMixin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_deleted = Column(Boolean, default=False)

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="posts")
    tags = relationship("Tags", secondary=post_tags, back_populates="posts")
