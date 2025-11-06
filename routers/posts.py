from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.orm import selectinload
from models.posts import Posts, post_tags
from models.tags import Tags
from routers.tags import validate_tags_exist
from schemas.posts import PostCreate, PostResponse, PostTagsCreate
from core.dependencies import get_session, get_current_user
from core.permissions import verify_post_owner

router = APIRouter()

@router.post("/create_post", response_model=PostResponse)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    # Crear el post sin tags primero
    post_dict = data.model_dump(exclude={"tags_ids"})
    nuevo_post = Posts(**post_dict, user_id=user.id)
    
    db.add(nuevo_post)
    await db.flush()  
    
    if data.tags_ids:
        
        tags_result = await db.execute(
            select(Tags).where(Tags.id.in_(data.tags_ids))
        )
        tags_encontrados = tags_result.scalars().all()
        
        if len(tags_encontrados) != len(data.tags_ids):
            tags_encontrados_ids = [tag.id for tag in tags_encontrados]
            tags_faltantes = set(data.tags_ids) - set(tags_encontrados_ids)
            raise HTTPException(
                status_code=404, 
                detail=f"Tags no encontrados: {tags_faltantes}"
            )
        
        stmt = insert(post_tags).values([
            {"post_id": nuevo_post.id, "tag_id": tag.id} 
            for tag in tags_encontrados
        ])
        await db.execute(stmt)
    
    await db.commit()
    
    # Recargar el post completo con sus tags
    post_completo = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == nuevo_post.id)
    )
    post_final = post_completo.scalar_one()
    
    return PostResponse.model_validate(post_final)


@router.get("/all_post", response_model=list[PostResponse])
async def list_posts(
    db: AsyncSession = Depends(get_session),
    user=Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100)
):
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
    # Verificar que el post exista y sea del usuario
    post_query = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == post_id)
        .where(Posts.user_id == current_user.id)
        .where(Posts.is_deleted.is_(False))
    )
    post = post_query.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    # Actualizar campos básicos
    post.title = data.title
    post.content = data.content

    # Manejar tags - FORMA CORRECTA
    if data.tags_ids is not None:
        # Limpiar tags existentes
        post.tags.clear()
        
        if data.tags_ids:
            # Obtener nuevos tags
            tags_result = await db.execute(
                select(Tags).where(Tags.id.in_(data.tags_ids))
            )
            nuevos_tags = tags_result.scalars().all()
            
            # Verificar que todos los tags existen
            if len(nuevos_tags) != len(data.tags_ids):
                tags_encontrados_ids = [tag.id for tag in nuevos_tags]
                tags_faltantes = set(data.tags_ids) - set(tags_encontrados_ids)
                raise HTTPException(
                    status_code=404, 
                    detail=f"Tags no encontrados: {tags_faltantes}"
                )
            
            # Asignar nuevos tags
            post.tags.extend(nuevos_tags)
    
    await db.commit()
    await db.refresh(post)
    
    # Recargar con tags
    post_actualizado = await db.execute(
        select(Posts)
        .options(selectinload(Posts.tags))
        .where(Posts.id == post.id)
    )
    return post_actualizado.scalar_one()

@router.delete("/{post_id}", response_model=str)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user)
):
    post_query = await db.execute(
        select(Posts)
        .where(Posts.id == post_id)
        .where(Posts.user_id == current_user.id)
        .where(Posts.is_deleted.is_(False))
    )
    post = post_query.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")
    
    post.is_deleted = True
    await db.commit()
    return "Post eliminado correctamente"