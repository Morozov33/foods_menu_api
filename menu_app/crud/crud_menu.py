from sqlmodel import SQLModel
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import func
from menu_app.submenu_model import Submenu
from menu_app.dish_model import Dish
from menu_app.crud.crud_base import Crud_Base


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

        return await db.get(model, id)
