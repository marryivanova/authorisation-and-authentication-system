import os
from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from database import get_db
from src.app import schemas, models
from src.app.auth import get_current_user
from src.app.helper import logging
from src.app.schemas import TokenData

router = APIRouter()

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


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.User, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    existing_user = (
        db.query(models.User)
        .filter(
            (models.User.email == user.email) | (models.User.username == user.username)
        )
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists.",
        )

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        role="user",
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        )

    return new_user
