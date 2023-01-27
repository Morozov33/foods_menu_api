import aioredis
from typing import AsyncIterator
from aioredis import from_url, Redis


async def init_redis(host: str) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{host}", decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()


def get_redis():

    redis = await aioredis.from_url(
            "redis://localhost",
            decode_responses=True
    )
    return redis
