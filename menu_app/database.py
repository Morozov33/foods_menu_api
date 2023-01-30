import os

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import delete

from menu_app.models.dish_model import Dish
from menu_app.models.menu_model import Menu
from menu_app.models.submenu_model import Submenu


DATABASE_URL = os.environ.get("DATABASE_URL")

# Create async engine for DB
async_engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
            async_engine,
            class_=AsyncSession,
            expire_on_commit=False
    )

    # Return async generator for database connection
    async with async_session() as session:
        yield session


async def clear_db():

    # Clear DB when app is shutdown
    async with AsyncSession(async_engine) as session:
        await session.execute(delete(Dish))
        await session.execute(delete(Submenu))
        await session.execute(delete(Menu))
        await session.commit()
