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
    user=Depends(get_current_user)
):
    
    post_dict = data.model_dump(exclude={"tags_ids"})  # <-- aquí usé model_dump en vez de data(exclude=...)
    nuevo_post = Posts(**post_dict, user_id=user.id)
    
    db.add(nuevo_post)
    await db.commit()
    await db.refresh(nuevo_post)  

    # Asigno los tags si los hay
    if data.tags_ids:
        tags_query = await db.execute(select(Tags).where(Tags.id.in_(data.tags_ids)))
        tags_encontrados = tags_query.scalars().all()
        nuevo_post.tags = tags_encontrados
        await db.commit()  
    
    # Recargo el post con sus tags para devolverlo completo
    post_con_tags = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == nuevo_post.id)
    )
    post_final = post_con_tags.scalar_one_or_none()
    if not post_final:
        raise HTTPException(status_code=404, detail="Post no encontrado tras creación")

    return PostResponse.model_validate(post_final)


@router.get("/all_post", response_model=list[PostResponse])
async def list_posts(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
    # Solo muestro posts del usuario actual que no estén eliminados
    consulta = (
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.is_deleted.is_(False)) 
        .where(Posts.user_id == user.id)
        .offset(skip)
        .limit(limit)
    )
    resultado = await db.execute(consulta)
    mis_posts = resultado.scalars().all()
    return mis_posts  


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: int,
    data: PostCreate,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user)  
):
    # Verifico que el post exista y sea del usuario
    post = await verify_post_owner(post_id, db)
    
    post.title = data.title
    post.content = data.content

    if data.tags_ids:
        tags_res = await db.execute(select(Tags).where(Tags.id.in_(data.tags_ids)))
        nuevos_tags = tags_res.scalars().all()
        post.tags = nuevos_tags  
    
    await db.commit()
    await db.refresh(post)

    # Devuelvo el post actualizado con sus tags
    resultado_final = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == post.id)
    )
    return resultado_final.scalar_one()


@router.delete("/{post_id}", status_code=204)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    post: Posts = Depends(verify_post_owner) 
):
    post.is_deleted = True
    await db.commit()
    