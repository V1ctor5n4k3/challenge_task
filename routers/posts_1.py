from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.posts import Posts
from models.tags import Tags
from schemas.posts import PostCreate, PostResponse
from core.dependencies import get_session, get_current_user
from core.permissions import verify_post_owner

router = APIRouter()


@router.post("/create_post", response_model=PostResponse)
async def create_post(
        data: PostCreate,
        db: AsyncSession = Depends(get_session),
        user=Depends(get_current_user)):
    
    post_data = data(exclude={"tags_ids"})
    post = Posts(**post_data, user_id=user.id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    
    if data.tags_ids:
        result = await db.execute(select(Tags).where(Tags.id.in_(data.tags_ids)))
        tags = result.scalars().all()
        post.tags = tags
        await db.commit   
        
    result = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == post.id)
    )
    post_tags = result.scalar_one()                              
                                         
    return PostResponse.model_validate(post_tags)


@router.get("/all_post", response_model=list[PostResponse])
async def list_posts(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    query = (
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.is_deleted == False, Posts.user_id == user.id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    data: PostCreate,
    db: AsyncSession = Depends(get_session),
):
    post = await verify_post_owner(post_id, db)
    
    post.title = data.title
    post.content = data.content
    
    if data.tags_ids:
        result = await db.execute(select(Tags).where(Tags.id.in_(data.tags_ids)))
        tags = result.scalars().all()
        post.tags = tags
    
    await db.commit()
    await db.refresh(post)
    
    result = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == post.id)
    )
    return result.scalar_one()

@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    post: Posts = Depends(verify_post_owner)
):
    post.is_deleted = True
    await db.commit()
    return "Se ha eliminado el Post correctamente"