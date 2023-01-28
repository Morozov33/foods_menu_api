from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from sqlmodel import SQLModel

from menu_app.cache.cache import Cache
from menu_app.crud.crud_base import Crud_Base
from menu_app.dish_model import Dish
from menu_app.dish_model import DishCreate
from menu_app.dish_model import DishUpdate


class DishCrud(Crud_Base):

    async def get_list(db: AsyncSession, model: SQLModel, id: int = None):
        cached_model = await Cache.get_data(f"{model.__name__.lower()}")

        if cached_model:
            return cached_model

        result = await db.execute(select(model).where(model.submenu_id == id))
        result_data = result.scalars().all()
        await Cache.save(f"{model.__name__.lower()}", result_data)

        return result_data

    async def create(
            db: AsyncSession,
            model: SQLModel,
            data: DishCreate,
            id: int
    ):
        result = model.from_orm(data)
        result.submenu_id = id
        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.clear(f"{model.__name__.lower()}")

        return result

    async def update(
            db: AsyncSession,
            model: SQLModel,
            data: DishUpdate,
            id: int
    ):
        result = await db.get(Dish, id)
        if not result:
            raise HTTPException(status_code=404, detail="dish not found")
        db_data = data.dict(exclude_unset=True)
        for key, value in db_data.items():
            setattr(result, key, value)
        result.price = float(result.price)
        db.add(result)
        await db.commit()
        await db.refresh(result)
        await Cache.save(f"{model.__name__.lower()}:{id}", result)
        await Cache.clear(f"{model.__name__.lower()}")

        return result
