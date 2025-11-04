from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.tags import Tags
from schemas.tags import TagsCreate, TagsResponse
from core.dependencies import get_session, get_current_user

router = APIRouter()


@router.post("/create_tag", response_model=TagsResponse)
async def create_tag(
        data: TagsCreate,
        db: AsyncSession = Depends(get_session),
        user=Depends(get_current_user)):

    tag = Tags(**data.dict())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


@router.get("/list_tags", response_model=list[TagsResponse])
async def list_tags(db: AsyncSession = Depends(get_session),
                    user=Depends(get_current_user),
                    skip: int = Query(0, ge=0),
                    limit: int = Query(10, le=100)
                    ):
    result = await db.execute(select(Tags).where(
        not Tags.is_deleted).offset(skip).limit(limit))
    return result.scalars().all()
