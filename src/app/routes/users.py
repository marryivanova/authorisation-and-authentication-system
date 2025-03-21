import os
import logging
from database import get_db
from sqlalchemy import select

from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, status

from src.app.middlewares import get_current_user
from src.app.schemas import TokenData, User, UserResponse

router = APIRouter()
logger = logging.getLogger(__name__)

template_dir = os.path.join(os.path.dirname(__file__), "../../frontend")
templates = Jinja2Templates(directory=template_dir)


@router.get("/admin")
async def admin_only(token_data: TokenData = Depends(get_current_user)):
    if token_data.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"message": "Admin access granted"}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/user")
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    existing_user = await db.execute(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )
    if existing_user.scalar():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists.",
        )
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        role=user.role,
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )

    logger.info(f"User {new_user.username} created successfully.")
    return new_user
