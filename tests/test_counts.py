from fastapi.testclient import TestClient
from sqlmodel import Session
from menu_app.main import Menu, Submenu, Dish


def test_count_submenus(session: Session, client: TestClient):
    menu = Menu(title="Menu 1", description="Menu description 1")
    session.add(menu)
    session.commit()
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
    session.add(submenu_1)
    session.add(submenu_2)
    session.commit()

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 2

    response = client.delete(
            f"/api/v1/menus/{menu.id}/submenus/{submenu_1.id}"
    )

    assert response.status_code == 200

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 1

    response = client.delete(
            f"/api/v1/menus/{menu.id}/submenus/{submenu_2.id}"
    )

    assert response.status_code == 200

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 0


def test_count_dishes(session: Session, client: TestClient):
    menu = Menu(title="Menu 1", description="Menu description 1")
    session.add(menu)
    session.commit()

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
    session.add(submenu_1)
    session.add(submenu_2)
    session.commit()

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
    session.add(dish_1)
    session.add(dish_2)
    session.add(dish_3)
    session.commit()

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 2
    assert data["dishes_count"] == 3

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 2

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_2.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 1

    response = client.delete(
            f"/api/v1/menus/1/submenus/{dish_2.submenu_id}/dishes/{dish_2.id}"
    )

    assert response.status_code == 200

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 2
    assert data["dishes_count"] == 2

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 1

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_2.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 1

    response = client.delete(
                    f"/api/v1/menus/{menu.id}/submenus/{dish_3.submenu.id}"
                    f"/dishes/{dish_3.id}"
    )

    assert response.status_code == 200

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 2
    assert data["dishes_count"] == 1

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 1

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_2.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 0

    response = client.delete(
                    f"/api/v1/menus/{menu.id}/submenus/{dish_1.submenu.id}"
                    f"/dishes/{dish_1.id}"
    )

    assert response.status_code == 200

    response = client.get(f"/api/v1/menus/{menu.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["submenus_count"] == 2
    assert data["dishes_count"] == 0

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 0

    response = client.get(f"/api/v1/menus/{menu.id}/submenus/{submenu_2.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["dishes_count"] == 0
