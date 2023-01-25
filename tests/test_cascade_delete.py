import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from menu_app.main import Menu, Submenu, Dish


@pytest.mark.asyncio
async def test_cascade_delete_menu(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    async_session.add(menu)
    await async_session.commit()

    submenu_1 = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )
    submenu_2 = Submenu(
            title="Submenu 2",
            description="Submenu description 2",
            menu_id=menu.id
    )
    async_session.add(submenu_1)
    async_session.add(submenu_2)
    await async_session.commit()

    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=submenu_1.id,
    )
    dish_2 = Dish(
        title="Dish 2",
        description="Dish description 2",
        price=33.15,
        submenu_id=submenu_1.id,
    )
    dish_3 = Dish(
        title="Dish 3",
        description="Dish description 3",
        price=5.20,
        submenu_id=submenu_2.id,
    )
    async_session.add(dish_1)
    async_session.add(dish_2)
    async_session.add(dish_3)
    await async_session.commit()

    response = await async_client.delete(f"menus/{menu.id}")
    menu_in_db = await async_session.get(Menu, menu.id)

    assert response.status_code == 200
    assert menu_in_db is None

    response = await async_client.get(f"menus/{menu.id}")

    assert response.status_code == 404

    response = await async_client.get(
            f"menus/{submenu_1.menu_id}/submenus/{submenu_1.id}"
    )
    submenu_1_in_db = await async_session.get(Submenu, submenu_1.id)

    assert response.status_code == 404
    assert submenu_1_in_db is None

    response = await async_client.get(
            f"menus/{submenu_2.menu_id}/submenus/{submenu_2.id}"
    )
    submenu_2_in_db = await async_session.get(Submenu, submenu_2.id)

    assert response.status_code == 404
    assert submenu_2_in_db is None

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{dish_1.submenu_id}"
            f"/dishes/{dish_1.id}",
    )
    dish_1_in_db = await async_session.get(Dish, dish_1.id)

    assert response.status_code == 404
    assert dish_1_in_db is None

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{dish_2.submenu_id}"
            f"/dishes/{dish_2.id}",
    )
    dish_2_in_db = await async_session.get(Dish, dish_2.id)

    assert response.status_code == 404
    assert dish_2_in_db is None

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{dish_3.submenu_id}"
            f"/dishes/{dish_3.id}",
    )
    dish_3_in_db = await async_session.get(Dish, dish_3.id)

    assert response.status_code == 404
    assert dish_3_in_db is None


@pytest.mark.asyncio
async def test_cascade_delete_submenu(
        async_session: AsyncSession,
        async_client: AsyncClient
):
    menu = Menu(title="Menu 1", description="Menu description 1")
    async_session.add(menu)
    await async_session.commit()

    submenu_1 = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=menu.id
    )
    submenu_2 = Submenu(
            title="Submenu 2",
            description="Submenu description 2",
            menu_id=menu.id
    )
    async_session.add(submenu_1)
    async_session.add(submenu_2)
    await async_session.commit()

    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=submenu_1.id,
    )
    dish_2 = Dish(
        title="Dish 2",
        description="Dish description 2",
        price=33.15,
        submenu_id=submenu_1.id,
    )
    dish_3 = Dish(
        title="Dish 3",
        description="Dish description 3",
        price=5.20,
        submenu_id=submenu_2.id,
    )
    async_session.add(dish_1)
    async_session.add(dish_2)
    async_session.add(dish_3)
    await async_session.commit()

    response = await async_client.delete(
            f"menus/{menu.id}/submenus/{submenu_1.id}"
    )

    assert response.status_code == 200

    response = await async_client.get(f"menus/{menu.id}")
    menu_in_db = await async_session.get(Menu, menu.id)

    assert response.status_code == 200
    assert menu_in_db is not None

    response = await async_client.get(
            f"menus/{submenu_1.menu_id}/submenus/{submenu_1.id}"
    )
    submenu_1_in_db = await async_session.get(Submenu, submenu_1.id)

    assert response.status_code == 404
    assert submenu_1_in_db is None

    response = await async_client.get(
            f"menus/{submenu_2.menu_id}/submenus/{submenu_2.id}"
    )
    submenu_2_in_db = await async_session.get(Submenu, submenu_2.id)

    assert response.status_code == 200
    assert submenu_2_in_db is not None

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{dish_1.submenu_id}"
            f"/dishes/{dish_1.id}",
    )
    dish_1_in_db = await async_session.get(Dish, dish_1.id)

    assert response.status_code == 404
    assert dish_1_in_db is None

    response = await async_client.get(
            f"/api/v1/menus/{menu.id}/submenus/{dish_2.submenu_id}"
            f"/dishes/{dish_2.id}",
    )
    dish_2_in_db = await async_session.get(Dish, dish_2.id)

    assert response.status_code == 404
    assert dish_2_in_db is None

    response = await async_client.get(
            f"menus/{menu.id}/submenus/{dish_3.submenu_id}"
            f"/dishes/{dish_3.id}",
    )
    dish_3_in_db = await async_session.get(Dish, dish_3.id)

    assert response.status_code == 200
    assert dish_3_in_db is not None
