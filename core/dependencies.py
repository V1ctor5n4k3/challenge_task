from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from jose import JWTError, jwt
from db.config import settings
from models.users import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = await db.get(User, int(user_id))
        if not user or user.is_deleted:
            raise HTTPException(
                status_code=404, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
