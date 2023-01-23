from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import select, delete
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from menu_app.database import get_session, engine
from menu_app.menu_model import (Menu, MenuRead, MenuCreate, MenuUpdate)
from menu_app.submenu_model import (Submenu, SubmenuRead,
                                    SubmenuCreate, SubmenuUpdate)
from menu_app.dish_model import Dish, DishRead, DishCreate, DishUpdate


app = FastAPI()


@app.on_event("shutdown")
async def on_shutdown():

    # Clear DB when app is shutdown
    async with AsyncSession(engine) as session:
        await session.exec(delete(Dish))
        await session.exec(delete(Submenu))
        await session.exec(delete(Menu))
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
    menus = await session.exec(select(Menu)).all()
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=MenuRead)
async def read_menu(
        *, menu_id: int,
        session: AsyncSession = Depends(get_session),
):
    menu = await session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")

    # Count all submenus
    menu.submenus_count = await session.exec(
            select(
                [func.count(Submenu.id)]
            ).where(Submenu.menu_id == menu_id)
    ).one()

    # Count all dishes, using Dish JOIN Submenu
    menu.dishes_count = await session.exec(
            select(
                [func.count(Dish.id)]
            ).join(Submenu).where(Submenu.menu_id == menu_id)
    ).one()
    return menu


@app.post("/api/v1/menus", response_model=MenuRead, status_code=201)
async def create_menu(
        *,
        session: AsyncSession = Depends(get_session),
        menu: MenuCreate,
):
    db_menu = await Menu.from_orm(menu)
    await session.add(db_menu)
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
        await setattr(db_menu, key, value)
    await session.add(db_menu)
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
    submenus = await session.exec(
            select(Submenu).where(Submenu.menu_id == menu_id)
    ).all()
    return submenus


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
    submenu.dishes_count = await session.exec(
            select(
                [func.count(Dish.id)]
            ).where(Dish.submenu_id == submenu_id)
    ).one()
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
    db_submenu = await Submenu.from_orm(submenu)
    db_submenu.menu_id = menu_id
    await session.add(db_submenu)
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
        await setattr(db_submenu, key, value)
    await session.add(db_submenu)
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
    dishes = await session.exec(
            select(Dish).where(Dish.submenu_id == submenu_id)
    ).all()
    return dishes


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
    db_dish = await Dish.from_orm(dish)
    db_dish.submenu_id = submenu_id
    await session.add(db_dish)
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
        await setattr(db_dish, key, value)
    await session.add(db_dish)
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
