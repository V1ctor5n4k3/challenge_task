from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class TagsBase(BaseModel):
    name: str

    @field_validator("name")
    def name_lenght(cls, n):
        if len(n) < 2:
            raise ValueError(
                "El nombre del Tag debe tener 2 o más caracteres.")
        return n


class TagsCreate(TagsBase):
    pass


class TagsResponse(TagsBase):
    id: int
    name: str
    
    model_config = {
        "from_attributes": True
    }
