import os
import pickle
import typing

from aioredis import from_url


class Cache():

    cache = from_url(
            os.environ.get('CACHE_URL'),
            encoding='latin-1',
            decode_responses=False)

    @classmethod
    async def save(cls, key: str, value: typing.Any):
        value = pickle.dumps(value)
        await cls.cache.set(key, value)

    @classmethod
    async def get_data(cls, key: str) -> typing.Any | None:
        data = await cls.cache.get(key)

        if data:
            return pickle.loads(data)

    @classmethod
    async def clear(cls, *args):
        if args:
            await cls.cache.delete(*args)
            return

        await cls.cache.flushdb(asynchronous=True)
