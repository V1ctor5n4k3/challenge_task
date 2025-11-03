from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.posts import Posts
from models.users import User
from core.dependencies import get_session, get_current_user


async def verify_post_owner(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
) -> Posts:
    result = await db.execute(select(Posts).where(
        Posts.id == post_id, not Posts.is_deleted))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para modificar este post")
    return post
