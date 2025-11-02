from sqlalchemy import Boolean, Column, DateTime, func
from sqlalchemy.orm import declared_attr


class At_Mixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class SoftDelMixin:
    is_deleted = Column(Boolean, default=False)

    @classmethod
    def not_deleted(cls, query):
        return query.filter(not cls.is_deleted)

    @declared_attr
    def __mapper_args__(cls):
        return {"confirm_deleted_rows": False}
