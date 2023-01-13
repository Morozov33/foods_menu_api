from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from menu_app.submenu_model import Submenu


class MenuBase(SQLModel):
    title: str
    description: str


class Menu(MenuBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    submenus: List["Submenu"] = Relationship(back_populates="menu")


class MenuRead(MenuBase):
    id: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(SQLModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
