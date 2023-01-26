from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select, delete
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from menu_app.database import get_session, async_engine
from menu_app.menu_model import (Menu, MenuRead, MenuCreate, MenuUpdate)
from menu_app.submenu_model import (Submenu, SubmenuRead,
                                    SubmenuCreate, SubmenuUpdate)
from menu_app.dish_model import Dish, DishRead, DishCreate, DishUpdate


app = FastAPI()


@app.on_event("shutdown")
async def on_shutdown():

    # Clear DB when app is shutdown
    async with AsyncSession(async_engine) as session:
        await session.execute(delete(Dish))
        await session.execute(delete(Submenu))
        await session.execute(delete(Menu))
        await session.commit()


@app.get("/")
async def root():

    # Welcome message from root
    return {
        "message": (
            """Hello, everyone!\
 It's simple food menu to contain the three tables:\
 Menu, Submenu and Dish. Let's play!"""
        )
    }


@app.get("/api/v1/menus", response_model=List[MenuRead])
async def read_menus(
        *,
        session: AsyncSession = Depends(get_session),
):
    menus = await session.execute(select(Menu))
    return menus.scalars().all()


@app.get("/api/v1/menus/{menu_id}", response_model=MenuRead)
async def read_menu(
        *, menu_id: int,
        session: AsyncSession = Depends(get_session),
):
    menu = await session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    # Count all submenus
    submenus_count = await session.execute(
            select(
                [func.count(Submenu.id)]
            ).where(Submenu.menu_id == menu_id)
    )
    menu.submenus_count = submenus_count.scalar()

    # Count all dishes, using Dish JOIN Submenu
    dishes_count = await session.execute(
            select(
                [func.count(Dish.id)]
            ).join(Submenu).where(Submenu.menu_id == menu_id)
    )
    menu.dishes_count = dishes_count.scalar()
    return menu


@app.post("/api/v1/menus", response_model=MenuRead, status_code=201)
async def create_menu(
        *,
        session: AsyncSession = Depends(get_session),
        menu: MenuCreate,
):
    db_menu = Menu.from_orm(menu)
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


@app.patch("/api/v1/menus/{menu_id}", response_model=MenuRead)
async def update_menu(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int,
        menu: MenuUpdate,
):
    db_menu = await session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    session.add(db_menu)
    await session.commit()
    await session.refresh(db_menu)
    return db_menu


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int,
):
    menu = await session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    await session.delete(menu)
    await session.commit()
    return {"ok": True}


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[SubmenuRead])
async def read_submenus(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int
):
    submenus = await session.execute(
            select(Submenu).where(Submenu.menu_id == menu_id)
    )
    return submenus.scalars().all()


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=SubmenuRead,
)
async def read_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int,
        submenu_id: int,
):
    submenu = await session.get(Submenu, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")

    # Count all dishes
    dishes_count = await session.execute(
            select(
                [func.count(Dish.id)]
            ).where(Dish.submenu_id == submenu_id)
    )
    submenu.dishes_count = dishes_count.scalars().one()
    return submenu


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=SubmenuRead,
    status_code=201,
)
async def create_submenu(
        *,
        menu_id: int,
        session: AsyncSession = Depends(get_session),
        submenu: SubmenuCreate,
):
    db_submenu = Submenu.from_orm(submenu)
    db_submenu.menu_id = menu_id
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=SubmenuUpdate,
)
async def update_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        submenu: SubmenuUpdate,
        submenu_id: int,
):
    db_submenu = await session.get(Submenu, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu_data = submenu.dict(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(db_submenu, key, value)
    session.add(db_submenu)
    await session.commit()
    await session.refresh(db_submenu)
    return db_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        submenu_id: int,
):
    submenu = await session.get(Submenu, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    await session.delete(submenu)
    await session.commit()
    return {"ok": True}


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[DishRead],
)
async def read_dishes(
        *,
        session: AsyncSession = Depends(get_session),
        submenu_id: int,
):
    dishes = await session.execute(
            select(Dish).where(Dish.submenu_id == submenu_id)
    )
    return dishes.scalars().all()


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishRead,
)
async def read_dish(
        *,
        session: AsyncSession = Depends(get_session),
        dish_id: int,
):
    dish = await session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@app.post(
        "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        response_model=DishRead,
        status_code=201,
)
async def create_dish(
        *,
        session: AsyncSession = Depends(get_session),
        dish: DishCreate,
        submenu_id: int,
):
    db_dish = Dish.from_orm(dish)
    db_dish.submenu_id = submenu_id
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishUpdate
)
async def update_dish(
        *,
        session: AsyncSession = Depends(get_session),
        dish: DishUpdate,
        dish_id: int,
):
    db_dish = await session.get(Dish, dish_id)
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    dish_data = dish.dict(exclude_unset=True)
    for key, value in dish_data.items():
        setattr(db_dish, key, value)
    db_dish.price = float(db_dish.price)
    session.add(db_dish)
    await session.commit()
    await session.refresh(db_dish)
    return db_dish


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(
        *,
        session: AsyncSession = Depends(get_session),
        dish_id: int,
):
    dish = await session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    await session.delete(dish)
    await session.commit()
    return {"ok": True}
