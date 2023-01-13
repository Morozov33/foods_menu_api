import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List
from fastapi import FastAPI, HTTPException
from menu_app.database import get_engine, connect_db_and_create_tables
from menu_app.menu_model import Menu, MenuRead, MenuCreate, MenuUpdate
from menu_app.submenu_model import (Submenu, SubmenuRead,
                                    SubmenuCreate, SubmenuUpdate)
from menu_app.dish_model import Dish, DishRead, DishCreate, DishUpdate
from sqlmodel import Session, select


app = FastAPI()


@app.on_event("startup")
def on_startup():

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Load envroinments variable
    env_path = os.path.join(BASE_DIR, '.env')
    load_dotenv(dotenv_path=env_path)

    # Connect to Postgres DB and create table
    connect_db_and_create_tables()


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/api/v1/menus/", response_model=List[MenuRead])
def read_menus():
    with Session(get_engine()) as session:
        menus = session.exec(select(Menu)).all()
        return menus


@app.get("/api/v1/menus/{menu_id}}/", response_model=MenuRead)
def read_menu(menu_id: int):
    with Session(get_engine()) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu not found")
        return menu


@app.post("/api/v1/menus/", response_model=MenuRead)
def create_menu(menu: MenuCreate):
    with Session(get_engine()) as session:
        db_menu = Menu.from_orm(menu)
        session.add(db_menu)
        session.commit()
        session.refresh(db_menu)
        return db_menu


@app.patch("/menus/{menu_id}", response_model=MenuRead)
def update_menu(menu_id: int, menu: MenuUpdate):
    with Session(get_engine()) as session:
        db_menu = session.get(Menu, menu_id)
        if not db_menu:
            raise HTTPException(status_code=404, detail="Menu not found")
        menu_data = menu.dict(exclude_unset=True)
        for key, value in menu_data.items():
            setattr(db_menu, key, value)
        session.add(db_menu)
        session.commit()
        session.refresh(db_menu)
        return db_menu


@app.delete("/api/v1//menus/{menu_id}/")
def delete_menu(menu_id: int):
    with Session(get_engine) as session:
        menu = session.get(Menu, menu_id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu not found")
        session.delete(menu)
        session.commit()
        return {"ok": True}
