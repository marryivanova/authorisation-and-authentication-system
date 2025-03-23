from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
import logging

from src.app.config import settings
from src.app.schemas import TokenData
from src.app.redis_client import redis_config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)


def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new access"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.auth.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a new refresh token"""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.auth.refresh_token_expire_days)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify the given token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.auth.secret_key, algorithms=[settings.auth.algorithm]
        )
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            logger.error("Invalid token: missing username or role")
            raise credentials_exception
        if role not in ["admin", "user"]:
            logger.error(f"Invalid role: {role}")
            raise credentials_exception

        access_token = token
        token_type = "bearer"

        token_data = TokenData(
            username=username,
            role=role,
            access_token=access_token,
            token_type=token_type,
        )
    except JWTError as e:
        logger.error(f"JWTError: {str(e)}")
        raise credentials_exception

    if redis_config.get(f"blacklist:{token}"):
        logger.error(f"Token in blacklist: {token}")
        raise credentials_exception

    return token_data


async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Get current user from the token"""
    return verify_token(token)
