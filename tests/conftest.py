import asyncio
import os

import pytest_asyncio
from aioredis import from_url
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from menu_app.database import get_session
from menu_app.main import app


BASE_PREFIX = f"{os.environ.get('HOST')}:{os.environ.get('PORT')}/api/v1/"

DATABASE_URL = os.environ.get("DATABASE_URL")


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="async_session", scope="function")
async def async_session() -> AsyncSession:

    async_engine = create_async_engine(
            DATABASE_URL,
            echo=True,
            future=True
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
            base_url=f'http://{BASE_PREFIX}',
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


@pytest_asyncio.fixture(name="cache", scope="function", autouse=True)
async def cache():

    yield

    cache = from_url(
            os.environ.get('CACHE_URL'),
            encoding='latin-1',
            decode_responses=False)
    await cache.flushdb(asynchronous=True)
