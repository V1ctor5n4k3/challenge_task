from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import get_password_hash, create_access_token
from core.security import verify_password
from core.dependencies import get_session
from schemas.users import UserCreate, Token, UserLogin
from models.users import User

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    if db_user.scalar():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    new_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar()
    if not db_user or not verify_password(user.password,
                                          db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}
