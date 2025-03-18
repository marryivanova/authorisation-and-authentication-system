import typing as t
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import (
    create_token,
    oauth2_scheme,
)
from app.config import settings
from app.schemas import TokenData
from app.redis_client import redis_config

router = APIRouter()


@router.post("/token", response_model=TokenData)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = create_token(data={"sub": form_data.username, "role": "user"})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    redis_config.set(
        f"blacklist:{token}", "true", ex=settings.access_token_expire_minutes * 60
    )
    return {"message": "Successfully logged out"}
