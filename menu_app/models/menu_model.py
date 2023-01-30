from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import SQLModel

if TYPE_CHECKING:
    from menu_app.submenu_model import Submenu


class MenuBase(SQLModel):

    # Base model for Menu
    title: str
    description: str
    submenus_count: Optional[int] = None
    dishes_count: Optional[int] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Menu 1",
                "description": "Menu description 1",
                "submenus_count": "3",
                "dishes_count": "7"
                }
        }


class Menu(MenuBase, table=True):

    # Main table model for Menu
    id: Optional[int] = Field(default=None, primary_key=True)
    submenus: List["Submenu"] = Relationship(
            sa_relationship_kwargs={"cascade": "delete"},
            back_populates="menu",
    )


class MenuRead(MenuBase):
    id: str


class MenuCreate(MenuBase):
    pass


class MenuUpdate(SQLModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
