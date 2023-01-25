import pytest_asyncio
from httpx import AsyncClient
from sqlmodel.pool import StaticPool
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from menu_app.main import app, get_session


@pytest_asyncio.fixture(name="async_session")
async def async_session():

    async_engine = create_async_engine(
            "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session


@pytest_asyncio.fixture(name='async_client')
async def async_client(async_session: AsyncSession) -> AsyncClient:

    async def get_session_override():
        yield async_session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
            app=app,
            base_url="http://127.0.0.1:8000/api/v1/"
    ) as client:
        yield client

    app.dependency_overrides.clear()
