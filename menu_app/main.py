import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from menu_app.database import get_engine, connect_db_and_create_tables
from menu_app.models import Menu, Submenu, Dish


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
    return {"message": f"Hello World!"}


@app.post("/menu/")
def create_menu(menu: Menu):
    with Session(get_engine()) as session:
        session.add(menu)
        session.commit()
        session.refresh(menu)
        return menu
