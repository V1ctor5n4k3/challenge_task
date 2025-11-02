from pydantic import BaseModel, field_validator
from typing import Optional


class CommentsBase(BaseModel):
    content: str

    @field_validator("content")
    def contentnot_empty(cls, c):
        if not c.strip():
            raise ValueError("El comentario no puede estar vacio.")
        return c


class CommentsCreate(CommentsBase):
    post_id: int


class CommentsResponse(CommentsBase):
    id: int
    post_id: int
    user_id: int
    created_at: str
    updated_at: str | None
