import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from menu_app.main import Menu


pytestmark = pytest.mark.asyncio


async def test_create_menu(async_client: AsyncClient):

    response = await async_client.post(
            "menus",
            json={"title": "Menu 1", "description": "Menu description 1"},
    )

    assert response.status_code == 201
    assert response.json().get("title") == "Menu 1"


async def test_create_menu_incomplete(async_client: AsyncClient):

    # No description is json
    response = await async_client.post(
            "menus",
            json={"title": "Menu 1"}
    )

    assert response.status_code == 422


async def test_create_menu_invalid(async_client: AsyncClient):

    # title has an invalid type
    response = await async_client.post(
        "menus",
        json={
            "title": {"message": "Menu 1"},
            "description": "Menu description 1",
        },
    )

    assert response.status_code == 422


async def test_read_menus(
        async_session: AsyncSession,
        async_client: AsyncClient,
):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    menu_2 = Menu(title="Menu 2", description="Menu description 1")
    async_session.add(menu_1)
    async_session.add(menu_2)
    await async_session.commit()

    response = await async_client.get("menus")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == menu_1.title
    assert data[0]["description"] == menu_1.description
    assert data[0]["id"] == str(menu_1.id)
    assert data[1]["title"] == menu_2.title
    assert data[1]["description"] == menu_2.description
    assert data[1]["id"] == str(menu_2.id)


async def test_read_menus_is_empty(
        async_session: AsyncSession,
        async_client: AsyncClient,
):
    response = await async_client.get("menus")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0


async def test_read_menu(
        async_session: AsyncSession,
        async_client: AsyncClient,
):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    async_session.add(menu_1)
    await async_session.commit()

    response = await async_client.get(f"menus/{menu_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == menu_1.title
    assert data["description"] == menu_1.description
    assert data["id"] == str(menu_1.id)


async def test_update_menu(
        async_session: AsyncSession,
        async_client: AsyncClient,
):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    async_session.add(menu_1)
    await async_session.commit()

    response = await async_client.patch(
            f"menus/{menu_1.id}",
            json={"title": "Update menu 1"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Update menu 1"
    assert data["description"] == "Menu description 1"
    assert data["id"] == str(menu_1.id)


async def test_delete_menu(
        async_session: AsyncSession,
        async_client: AsyncClient,
):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    async_session.add(menu_1)
    await async_session.commit()

    response = await async_client.delete(f"menus/{menu_1.id}")
    menu_in_db = await async_session.get(Menu, menu_1.id)

    assert response.status_code == 200
    assert menu_in_db is None
