from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel import SQLModel

from menu_app.cache.cache import Cache


class Crud_Base():

    async def get(db: AsyncSession, model: SQLModel, id: int):
        cached_model = await Cache.get_data(f"{model.__name__.lower()}:{id}")

        if cached_model:
            return cached_model

        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        await Cache.save(f"{model.__name__.lower()}:{id}", result)
        return result

    async def get_list(db: AsyncSession, model: SQLModel):
        cached_model = await Cache.get_data(f"{model.__name__.lower()}")

        if cached_model:
            return cached_model

        result = await db.execute(select(model))
        result_data = result.scalars().all()
        await Cache.save(f"{model.__name__.lower()}", result)

        return result_data

    async def create(db: AsyncSession, model: SQLModel, data):
        result = model.from_orm(data)
        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.clear(f"{model.__name__.lower()}")

        return result

    async def update(db: AsyncSession, model: SQLModel, data, id: int):
        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        data = data.dict(exclude_unset=True)

        for key, value in data.items():
            setattr(result, key, value)

        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.save(f"{model.__name__.lower()}:{id}", result)
        await Cache.clear(f"{model.__name__.lower()}s")

        return result

    async def delete(db: AsyncSession, model: SQLModel, id: int):
        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        await db.delete(result)
        await db.commit()
        await Cache.clear()
        return {"ok": True}
