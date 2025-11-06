from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.tags import Tags
from schemas.tags import TagsCreate, TagsResponse
from core.dependencies import get_session, get_current_user

router = APIRouter()

async def validate_tags_exist(db: AsyncSession, tag_ids: list[int]) -> list:
    if not tag_ids:
        return []
    
    # Obtener todos los tags que existen con esos IDs
    result = await db.execute(select(Tags.id).where(Tags.id.in_(tag_ids)))
    existing_ids = set(result.scalars().all())
    
    # Encontrar los que NO existen
    missing_ids = set(tag_ids) - existing_ids
    if missing_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Estos tag IDs no existen: {sorted(missing_ids)}"
        )
    
    tags_result = await db.execute(select(Tags).where(Tags.id.in_(tag_ids)))
    return tags_result.scalars().all()


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
        Tags.is_deleted.is_(False)).offset(skip).limit(limit))
    return result.scalars().all()


@router.delete("/{tag_id}", response_model=str)
async def delete_post(
    tag_id: int,
    db: AsyncSession = Depends(get_session),
    current_user=Depends(get_current_user)
):
    tag_query = await db.execute(
        select(Tags)
        .where(Tags.id == tag_id)
        .where(Tags.is_deleted.is_(False))
    )
    tag = tag_query.scalar_one_or_none()
    
    if not tag:
        raise HTTPException(status_code=404, detail="Etiqueta no encontrada")
    
    tag.is_deleted = True
    await db.commit()
    return "Etiqueta eliminada correctamente"
 