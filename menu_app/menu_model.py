from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from menu_app.submenu_model import Submenu


class MenuBase(SQLModel):

    # Base model for Menu
    title: str
    description: str
    submenus_count: Optional[int] = None
    dishes_count: Optional[int] = None


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
