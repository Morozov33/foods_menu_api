import pytest
import os
from httpx import AsyncClient
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from menu_app.main import app
from menu_app.database import get_session


os.environ.get("DATABASE_URL")

@pytest.fixture(name="session")
async def session():

    async_engine = create_async_engine(
            "sqlite+aiosqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(async_engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture(name="client")
async def client(session: AsyncSession):

    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    async with AsyncClient(app=app, base_url="http:/") as client:
        yield client
    app.dependency_overrides.clear()
