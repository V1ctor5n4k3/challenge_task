from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.dependencies import get_session, get_current_user
from core.security import get_password_hash
from models.users import User
from schemas.users import UserResponse, UserCreate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/list_users", response_model=list[UserResponse])
async def list_users(db: AsyncSession = Depends(get_session),
                     skip: int = Query(0, ge=0),
                     limit: int = Query(10, le=100)):

    result = await db.execute(select(User).where(
        not User.is_deleted).offset(skip).limit(limit))

    return result.scalars().all()
