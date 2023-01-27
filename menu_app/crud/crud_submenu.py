from sqlmodel import SQLModel
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlalchemy import func
from menu_app.submenu_model import SubmenuCreate
from menu_app.dish_model import Dish
from menu_app.crud.crud_base import Crud_Base


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
        return await db.get(model, id)

    async def get_list(db: AsyncSession, model: SQLModel, id: int = None):
        result = await db.execute(select(model).where(model.menu_id == id))
        return result.scalars().all()

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
        return result
