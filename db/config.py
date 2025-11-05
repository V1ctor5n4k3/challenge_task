from pydantic import BaseModel, Field, validator
import os

class Settings(BaseModel):
    DATABASE_URL: str = Field(
        default=os.getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:postgres@localhost:5432/challenge_db"
        )
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "123")
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 15

    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if "postgresql://" in v and "+asyncpg" not in v:
            v = v.replace("postgresql://", "postgresql+asyncpg://")
        elif "postgres://" in v:
            v = v.replace("postgres://", "postgresql+asyncpg://")
        return v

settings = Settings()

