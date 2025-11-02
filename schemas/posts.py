from pydantic import BaseModel, field_validator
from typing import Optional, List


class PostBase(BaseModel):
    title: str
    content: str

    @field_validator("title")
    def title_lenght(cls, t):
        if len(t) < 5:
            raise ValueError("El título debe tener 5 o más caracteres.")
        return t


class PostCreate(PostBase):
    tags_ids: Optional[List[int]] = []


class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: str
    updated_at: str | None
    tags: List[int]
