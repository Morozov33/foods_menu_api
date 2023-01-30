from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from menu_app.menu_model import Menu
    from menu_app.dish_model import Dish


class SubmenuBase(SQLModel):

    # Base model for Submenu
    title: str = Field(index=True)
    description: str
    menu_id: Optional[int] = Field(default=None, foreign_key="menu.id")
    dishes_count: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Submenu 1",
                "description": "Submenu description 1",
                "menu_id": "1",
                "dishes_count": "3"
                }
        }


class Submenu(SubmenuBase, table=True):

    # Main table model for Submenu
    id: Optional[int] = Field(default=None, primary_key=True)
    menu: Optional["Menu"] = Relationship(back_populates="submenus")
    dishes: List["Dish"] = Relationship(
            sa_relationship_kwargs={"cascade": "delete"},
            back_populates="submenu",
    )


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuRead(SubmenuBase):
    id: str


class SubmenuUpdate(SQLModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
