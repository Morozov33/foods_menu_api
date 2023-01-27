import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from menu_app.main import Menu, Submenu, Dish


pytestmark = pytest.mark.asyncio


async def test_create_dish(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )
    async_session.add(submenu)
    async_session.add(menu)
    await async_session.commit()

    response = await async_client.post(
                f"menus/{menu.id}/submenus/{submenu.id}/dishes",
                json={
                    "title": "Dish 1",
                    "description": "Dish description 1",
                    "price": 99.99
                },
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Dish 1"
    assert data["description"] == "Dish description 1"
    assert data["price"] == "99.99"


async def test_create_dish_incomplete(async_client: AsyncClient):
    # No description
    response = await async_client.post(
            "menus/1/submenus/1/dishes",
            json={"title": "Dish 1"}
    )

    assert response.status_code == 422


async def test_create_dish_invalid(async_client: AsyncClient):
    # title has an invalid type
    response = await async_client.post(
        "menus/1/submenus/1/dishes",
        json={
            "title": {"message": "Dish 1"},
            "description": "Dish description 1",
        },
    )

    assert response.status_code == 422


async def test_read_dishes(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )

    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=submenu.id,
    )
    dish_2 = Dish(
        title="Dish 2",
        description="Dish description 2",
        price=33.15,
        submenu_id=submenu.id,
    )
    async_session.add(submenu)
    async_session.add(menu)
    async_session.add(dish_1)
    async_session.add(dish_2)
    await async_session.commit()

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{submenu.id}/dishes"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == dish_1.title
    assert data[0]["description"] == dish_1.description
    assert data[0]["id"] == str(dish_1.id)
    assert data[0]["price"] == "99.99"
    assert data[1]["title"] == dish_2.title
    assert data[1]["description"] == dish_2.description
    assert data[1]["id"] == str(dish_2.id)
    assert data[1]["price"] == "33.15"


async def test_read_dishes_is_empty(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=1
    )
    async_session.add(menu)
    async_session.add(submenu)
    await async_session.commit()

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{submenu.id}/dishes"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0


async def test_read_dish(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )
    async_session.add(menu)
    async_session.add(submenu)
    await async_session.commit()

    dish = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=submenu.id,
    )
    async_session.add(dish)
    await async_session.commit()

    response = await async_client.get(
        f"menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == dish.title
    assert data["description"] == dish.description
    assert data["price"] == "99.99"


async def test_update_dish(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )
    dish = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=submenu.id
    )
    async_session.add(dish)
    async_session.add(menu)
    async_session.add(submenu)
    await async_session.commit()

    response = await async_client.patch(
            f"menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}",
            json={"title": "Update dish 1"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Update dish 1"
    assert data["description"] == "Dish description 1"
    assert data["price"] == "99.99"


async def test_delete_dish(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )
    dish = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=submenu.id
    )
    async_session.add(dish)
    async_session.add(menu)
    async_session.add(submenu)
    await async_session.commit()

    response = await async_client.delete(
            f"menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}",
    )
    dish_in_db = await async_session.get(Dish, dish.id)

    assert response.status_code == 200
    assert dish_in_db is None
