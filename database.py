from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.app.config import settings


SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{settings.database.username}:{settings.database.password}@"
    f"{settings.database.hostname}:{settings.database.port}/{settings.database.name}"
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
