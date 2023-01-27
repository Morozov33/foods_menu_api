import os
import pytest_asyncio
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from menu_app.database import get_session
from menu_app.main import app


@pytest_asyncio.fixture(name="async_session", scope="function", autouse=True)
async def async_session() -> AsyncSession:

    async_engine = create_async_engine(
            os.environ.get('DATABASE_URL'),
            echo=True,
            future=True
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session


@pytest_asyncio.fixture(name='async_client', autouse=True)
async def async_client(async_session: AsyncSession) -> AsyncClient:

    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
            app=app,
            base_url=f'http://{os.environ.get("BASE_PREFIX")}',
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(name="clear_db", scope="function", autouse=True)
async def clear_db():

    yield

    async_engine = create_async_engine(
            os.environ.get('DATABASE_URL'),
            echo=True,
            future=True
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()
