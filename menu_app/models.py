from typing import Optional, List

from sqlmodel import Field, Relationship, SQLModel


class Menu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    submenus: List["Submenu"] = Relationship(back_populates="menu")


class Submenu(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    menu_id: Optional[int] = Field(default=None, foreign_key="menu.id")
    menu: Optional[Menu] = Relationship(back_populates="menus")
    dishes: List["Dish"] = Relationship(back_populates="submenu")


class Dish(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    submenu_id: Optional[int] = Field(default=None, foreign_key="submenu.id")
    submenu: Optional[Menu] = Relationship(back_populates="dishes")
