import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select, delete
from sqlalchemy import func
from menu_app.database import get_session, engine
from menu_app.menu_model import (Menu, MenuRead, MenuCreate, MenuUpdate)
from menu_app.submenu_model import (Submenu, SubmenuRead,
                                    SubmenuCreate, SubmenuUpdate)
from menu_app.dish_model import Dish, DishRead, DishCreate, DishUpdate


app = FastAPI()


@app.on_event("startup")
def on_startup():

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load envroinments variable
    env_path = os.path.join(BASE_DIR, '.env')
    load_dotenv(dotenv_path=env_path)


@app.on_event("shutdown")
def on_shutdown():

    # Clear DB
    with Session(engine) as session:
        session.exec(delete(Dish))
        session.exec(delete(Submenu))
        session.exec(delete(Menu))
        session.commit()


@app.get("/")
def root():
    return {
        "message": (
            """Hello, everyone!\
 It's simple food menu to contain the three tables:\
 Menu, Submenu and Dish. Let's play!"""
        )
    }


@app.get("/api/v1/menus", response_model=List[MenuRead])
def read_menus(
        *,
        session: Session = Depends(get_session),
):
    menus = session.exec(select(Menu)).all()
    return menus


@app.get("/api/v1/menus/{menu_id}", response_model=MenuRead)
def read_menu(
        *, menu_id: int,
        session: Session = Depends(get_session),
):
    menu = session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu.submenus_count = session.exec(
            select(
                [func.count(Submenu.id)]
            ).where(Submenu.menu_id == menu_id)
    ).one()
    menu.dishes_count = session.exec(
            select(
                [func.count(Dish.id)]
            ).where(Dish.menu_id == menu_id)
    ).one()
    return menu


@app.post("/api/v1/menus", response_model=MenuRead, status_code=201)
def create_menu(
        *,
        session: Session = Depends(get_session),
        menu: MenuCreate,
):
    db_menu = Menu.from_orm(menu)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


@app.patch("/api/v1/menus/{menu_id}", response_model=MenuRead)
def update_menu(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        menu: MenuUpdate,
):
    db_menu = session.get(Menu, menu_id)
    if not db_menu:
        raise HTTPException(status_code=404, detail="menu not found")
    menu_data = menu.dict(exclude_unset=True)
    for key, value in menu_data.items():
        setattr(db_menu, key, value)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
):
    menu = session.get(Menu, menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="menu not found")
    session.delete(menu)
    session.commit()
    return {"ok": True}


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[SubmenuRead])
def read_submenus(*, session: Session = Depends(get_session), menu_id: int):
    submenus = session.exec(
            select(Submenu).where(Submenu.menu_id == menu_id)
    ).all()
    return submenus


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=SubmenuRead,
)
def read_submenu(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        submenu_id: int,
):
    submenu = session.get(Submenu, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu.dishes_count = session.exec(
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
def create_submenu(
        *,
        menu_id: int,
        session: Session = Depends(get_session),
        submenu: SubmenuCreate,
):
    db_submenu = Submenu.from_orm(submenu)
    db_submenu.menu_id = menu_id
    session.add(db_submenu)
    session.commit()
    session.refresh(db_submenu)
    return db_submenu


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}",
    response_model=SubmenuUpdate,
)
def update_submenu(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        submenu: SubmenuUpdate,
        submenu_id: int,
):
    db_submenu = session.get(Submenu, submenu_id)
    if not db_submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    submenu_data = submenu.dict(exclude_unset=True)
    for key, value in submenu_data.items():
        setattr(db_submenu, key, value)
    session.add(db_submenu)
    session.commit()
    session.refresh(db_submenu)
    return db_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        submenu_id: int,
):
    submenu = session.get(Submenu, submenu_id)
    if not submenu:
        raise HTTPException(status_code=404, detail="submenu not found")
    session.delete(submenu)
    session.commit()
    return {"ok": True}


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
    response_model=List[DishRead],
)
def read_dishes(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        submenu_id: int,
):
    dishes = session.exec(
            select(Dish).where(Dish.submenu_id == submenu_id)
    ).all()
    return dishes


@app.get(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishRead,
)
def read_dish(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        submenu_id: int,
        dish_id: int,
):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    return dish


@app.post(
        "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
        response_model=DishRead,
        status_code=201,
)
def create_dish(
        *,
        session: Session = Depends(get_session),
        dish: DishCreate,
        menu_id: int,
        submenu_id: int,
):
    db_dish = Dish.from_orm(dish)
    db_dish.menu_id = menu_id
    db_dish.submenu_id = submenu_id
    session.add(db_dish)
    session.commit()
    session.refresh(db_dish)
    return db_dish


@app.patch(
    "/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}",
    response_model=DishUpdate
)
def update_dish(
        *,
        session: Session = Depends(get_session),
        dish: DishUpdate,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
):
    db_dish = session.get(Dish, dish_id)
    if not db_dish:
        raise HTTPException(status_code=404, detail="dish not found")
    dish_data = dish.dict(exclude_unset=True)
    for key, value in dish_data.items():
        setattr(db_dish, key, value)
    session.add(db_dish)
    session.commit()
    session.refresh(db_dish)
    return db_dish


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(
        *,
        session: Session = Depends(get_session),
        menu_id: int,
        submenu_id: int,
        dish_id: int,
):
    dish = session.get(Dish, dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="dish not found")
    session.delete(dish)
    session.commit()
    return {"ok": True}
