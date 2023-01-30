from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel import SQLModel

from menu_app.cache import Cache
from menu_app.crud.crud_base import Crud_Base
from menu_app.models.dish_model import Dish
from menu_app.models.submenu_model import Submenu


class MenuCrud(Crud_Base):

    @staticmethod
    async def count_submenus(db: AsyncSession, model: SQLModel):
        result = await db.execute(
                select([func.count(Submenu.id)]
                       ).where(Submenu.menu_id == model.id)
                 )
        model.submenus_count = result.scalars().one()

    @staticmethod
    async def count_dishes(db: AsyncSession, model: SQLModel):
        result = await db.execute(
                select(
                    [func.count(Dish.id)]
                ).join(Submenu).where(Submenu.menu_id == model.id)
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
        await cls.count_submenus(db, result)
        await cls.count_dishes(db, result)
        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.save(f"{model.__name__.lower()}:{id}", result)

        return await db.get(model, id)

    @classmethod
    async def get_list(cls, db: AsyncSession, model: SQLModel):
        cached_model = await Cache.get_data(f"{model.__name__.lower()}")

        if cached_model:
            return cached_model

        menus = await db.execute(select(model))
        result_data = list()
        for menu in menus.scalars().all():
            await cls.count_submenus(db, menu)
            await cls.count_dishes(db, menu)
            db.add(menu)
            await db.commit()
            await db.refresh(menu)

            result_data.append(menu)

        await Cache.save(f"{model.__name__.lower()}", result_data)

        return result_data
