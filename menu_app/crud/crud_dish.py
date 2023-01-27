from sqlmodel import SQLModel
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from menu_app.dish_model import Dish, DishCreate, DishUpdate
from menu_app.crud.crud_base import Crud_Base


class DishCrud(Crud_Base):

    async def get_list(db: AsyncSession, model: SQLModel, id: int = None):
        result = await db.execute(select(model).where(model.submenu_id == id))
        return result.scalars().all()

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
        return result
