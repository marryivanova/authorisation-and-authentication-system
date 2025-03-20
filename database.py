from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.app.config import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.database.username}:{settings.database.password}@"
    f"{settings.database.hostname}:{settings.database.port}/{settings.database.name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
