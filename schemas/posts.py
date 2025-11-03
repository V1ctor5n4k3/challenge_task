from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from schemas.tags import TagsResponse


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
    created_at: datetime
    updated_at: datetime | None
    tags: List[TagsResponse]
    
    model_config = {
        "from_attributes": True
    }
