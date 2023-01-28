from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel import SQLModel

from menu_app.cache.cache import Cache
from menu_app.crud.crud_base import Crud_Base
from menu_app.dish_model import Dish
from menu_app.submenu_model import SubmenuCreate


class SubmenuCrud(Crud_Base):

    @staticmethod
    async def count_dishes(db: AsyncSession, model: SQLModel):
        result = await db.execute(
                select(
                    [func.count(Dish.id)]
                ).where(Dish.submenu_id == model.id)
        )
        model.dishes_count = result.scalars().one()

    @classmethod
    async def get(cls, db: AsyncSession, model: SQLModel, id: int):
        cached_model = await Cache.get_data(f"{model.__name__.lower()}:{id}")

        if cached_model:
            return cached_model

        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        await cls.count_dishes(db, result)
        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.save(f"{model.__name__.lower()}:{id}", result)

        return await db.get(model, id)

    async def get_list(db: AsyncSession, model: SQLModel, id: int = None):
        cached_model = await Cache.get_data(f"{model.__name__.lower()}")

        if cached_model:
            return cached_model

        result = await db.execute(select(model).where(model.menu_id == id))
        result_data = result.scalars().all()
        await Cache.save(f"{model.__name__.lower()}", result_data)

        return result_data

    async def create(
            db: AsyncSession,
            model: SQLModel,
            data: SubmenuCreate,
            id: int
    ):
        result = model.from_orm(data)
        result.menu_id = id
        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.clear(f"{model.__name__.lower()}")

        return result
