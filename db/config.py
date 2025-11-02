from pydantic import BaseModel
import os


class Settings(BaseModel):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/challenge_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "123")
    ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_MINUTES: int = 15


settings = Settings()


