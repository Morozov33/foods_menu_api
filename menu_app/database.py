import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


# Create async engine for DB
engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
    )

    # Return async generator for database connection
    async with async_session as session:
        yield session
