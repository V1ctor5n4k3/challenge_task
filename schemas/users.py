from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    full_name: str
    email: EmailStr

    @field_validator("full_name")
    def name_not_empty(cls, n):
        if not n.strip():
            raise ValueError("El nombre no puede estar vacio.")
        return n


class UserCreate(UserBase):
    password: str

    @field_validator("password")
    def password_lenght(cls, n):
        if len(n) < 8:
            raise ValueError("La contraseña debe tener 8 o más caracteres.")
        return n


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime | None


class Token(BaseModel):
    access_token: str
    token_type: str
