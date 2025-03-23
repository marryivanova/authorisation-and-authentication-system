from jose import jwt, JWTError
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.app.models import User
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from database import get_db
from src.app.middlewares import (
    create_token,
    oauth2_scheme,
    verify_password,
)
from src.app.config import settings
from src.app.schemas import TokenData
from src.app.redis_client import redis_config

router = APIRouter()
security = HTTPBearer()


@router.post("/token", response_model=TokenData)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: AsyncSession = Depends(get_db),
):
    async with db.begin():
        stmt = select(User).filter(User.username == form_data.username)
        result = await db.execute(stmt)
        user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_token(data={"sub": user.username, "role": user.role})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,
        "role": user.role,
    }


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    redis_config.set(
        f"blacklist:{token}", "true", ex=settings.auth.access_token_expire_minutes * 60
    )
    return {"message": "Successfully logged out"}


@router.post("/refresh")
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    refresh_token = credentials.credentials
    if redis_config.get(f"blacklist:{refresh_token}"):
        raise HTTPException(status_code=400, detail="Token is blacklisted")

    try:
        payload = jwt.decode(
            refresh_token,
            settings.auth.secret_key,
            algorithms=[settings.auth.algorithm],
        )
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=400, detail="Invalid token")

        access_token = create_token(data={"sub": username, "role": role})
        return {"access_token": access_token, "token_type": "bearer"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
