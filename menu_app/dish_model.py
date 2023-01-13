from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from menu_app.submenu_model import Submenu


class DishBase(SQLModel):
    title: str = Field(index=True)
    description: str
    price: float
    submenu_id: Optional[int] = Field(default=None, foreign_key="submenu.id")


class Dish(DishBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submenu: Optional["Submenu"] = Relationship(back_populates="dishes")


class DishRead(DishBase):
    id: int
    title: str
    description: str


class DishCreate(DishBase):
    pass


class DishUpdate(SQLModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    submenu_id: Optional[int] = None
