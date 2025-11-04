from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.comments import Comments
from models.posts import Posts
from models.users import User
from schemas.comments import CommentsCreate, CommentsResponse
from core.dependencies import get_session, get_current_user

router = APIRouter()


@router.post("/create_comment", response_model=CommentsResponse)
async def create_comment(
        data: CommentsCreate,
        db: AsyncSession = Depends(get_session),
        user=Depends(get_current_user)):
    comment = Comments(**data.dict(), user_id=user.id)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    result = await db.execute(
        select(Comments)
        .options(
            selectinload(Comments.author),
            selectinload(Comments.posts)
        )
        .where(Comments.id == comment.id)
    )
    comment_with_relations = result.scalar_one()

    return CommentsResponse.model_validate(comment_with_relations)
   


@router.get("/list_comments", response_model=list[CommentsResponse])
async def list_comments(db: AsyncSession = Depends(get_session),
                        skip: int = Query(0, ge=0),
                        limit: int = Query(10, le=100)
                        ):
    result = await db.execute(select(Comments).where(
        Comments.is_deleted == False).offset(skip).limit(limit))

    return result.scalars().all()
