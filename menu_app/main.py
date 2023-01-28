from typing import List

from fastapi import Depends
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.cache.cache import Cache
from menu_app.crud.crud_dish import DishCrud
from menu_app.crud.crud_menu import MenuCrud
from menu_app.crud.crud_submenu import SubmenuCrud
from menu_app.database import clear_db
from menu_app.database import get_session
from menu_app.dish_model import Dish
from menu_app.dish_model import DishCreate
from menu_app.dish_model import DishRead
from menu_app.dish_model import DishUpdate
from menu_app.menu_model import Menu
from menu_app.menu_model import MenuCreate
from menu_app.menu_model import MenuRead
from menu_app.menu_model import MenuUpdate
from menu_app.submenu_model import Submenu
from menu_app.submenu_model import SubmenuCreate
from menu_app.submenu_model import SubmenuRead
from menu_app.submenu_model import SubmenuUpdate

app = FastAPI()


@app.on_event("shutdown")
async def on_shutdown():
    await clear_db()
    await Cache.clear()


@app.get("/")
async def root():
    # Welcome message from root
    return {"message": ("Hello, everyone! It's simple food menu. Let's play!")}


@app.get("/api/v1/menus", response_model=List[MenuRead])
async def read_menus(
        *,
        session: AsyncSession = Depends(get_session),
):
    return await MenuCrud.get_list(session, Menu)


@app.get("/api/v1/menus/{menu_id}", response_model=MenuRead)
async def read_menu(
        *, menu_id: int,
        session: AsyncSession = Depends(get_session),
):
    return await MenuCrud.get(session, Menu, menu_id)


@app.post("/api/v1/menus", response_model=MenuRead, status_code=201)
async def create_menu(
        *,
        session: AsyncSession = Depends(get_session),
        data: MenuCreate,
):
    return await MenuCrud.create(session, Menu, data)


@app.patch("/api/v1/menus/{menu_id}", response_model=MenuRead)
async def update_menu(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int,
        data: MenuUpdate,
):
    return await MenuCrud.update(session, Menu, data, menu_id)


@app.delete("/api/v1/menus/{menu_id}")
async def delete_menu(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int,
):
    return await MenuCrud.delete(session, Menu, menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[SubmenuRead])
async def read_submenus(
        *,
        session: AsyncSession = Depends(get_session),
        menu_id: int
):
    return await SubmenuCrud.get_list(session, Submenu, menu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=SubmenuRead,
)
async def read_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        submenu_id: int,
):
    return await SubmenuCrud.get(session, Submenu, submenu_id)


@app.post(
    "/api/v1/menus/{menu_id}/submenus",
    response_model=SubmenuRead,
    status_code=201,
)
async def create_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        data: SubmenuCreate,
        menu_id: int,
):
    return await SubmenuCrud.create(session, Submenu, data, menu_id)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=SubmenuUpdate,
)
async def update_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        data: SubmenuUpdate,
        submenu_id: int,
):
    return await SubmenuCrud.update(session, Submenu, data, submenu_id)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(
        *,
        session: AsyncSession = Depends(get_session),
        submenu_id: int,
):
    return await SubmenuCrud.delete(session, Submenu, submenu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[DishRead],
)
async def read_dishes(
        *,
        session: AsyncSession = Depends(get_session),
        submenu_id: int,
):
    return await DishCrud.get_list(session, Dish, submenu_id)


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishRead,
)
async def read_dish(
        *,
        session: AsyncSession = Depends(get_session),
        dish_id: int,
):
    return await DishCrud.get(session, Dish, dish_id)


@app.post(
        "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        response_model=DishRead,
        status_code=201,
)
async def create_dish(
        *,
        session: AsyncSession = Depends(get_session),
        data: DishCreate,
        submenu_id: int,
):
    return await DishCrud.create(session, Dish, data, submenu_id)


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishUpdate
)
async def update_dish(
        *,
        session: AsyncSession = Depends(get_session),
        data: DishUpdate,
        dish_id: int,
):
    return await DishCrud.update(session, Dish, data, dish_id)


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(
        *,
        session: AsyncSession = Depends(get_session),
        dish_id: int,
):
    return await DishCrud.delete(session, Dish, dish_id)
