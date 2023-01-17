from fastapi.testclient import TestClient
from sqlmodel import Session
from menu_app.main import Menu, Submenu, Dish


def test_create_dish(client: TestClient):
    response = client.post(
                "/api/v1/menus/1/submenus/1/dishes",
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


def test_create_dish_incomplete(client: TestClient):
    # No description
    response = client.post(
            "/api/v1/menus/1/submenus/1/dishes",
            json={"title": "Dish 1"}
    )

    assert response.status_code == 422


def test_create_dish_invalid(client: TestClient):
    # title has an invalid type
    response = client.post(
        "/api/v1/menus/1/submenus/1/dishes",
        json={
            "title": {"message": "Dish 1"},
            "description": "Dish description 1",
        },
    )

    assert response.status_code == 422


def test_read_dishes(session: Session, client: TestClient):
    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=1,
    )
    dish_2 = Dish(
        title="Dish 2",
        description="Dish description 2",
        price=33.15,
        submenu_id=1,
    )
    session.add(dish_1)
    session.add(dish_2)
    session.commit()

    response = client.get(
            f"/api/v1/menus/1/submenus/{dish_1.submenu_id}/dishes"
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


def test_read_dishes_is_empty(session: Session, client: TestClient):
    menu = Menu(title="Menu 1", description="Menu description 1")
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=1
    )
    session.add(menu)
    session.add(submenu)
    session.commit()

    response = client.get(
            f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes"
    )
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 0


def test_read_dish(session: Session, client: TestClient):
    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=1,
    )
    session.add(dish_1)
    session.commit()

    response = client.get(
        f"/api/v1/menus/1/submenus/{dish_1.submenu_id}/dishes/{dish_1.id}"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == dish_1.title
    assert data["description"] == dish_1.description
    assert data["price"] == "99.99"
    assert data["id"] == str(dish_1.id)


def test_update_dish(session: Session, client: TestClient):
    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=1
    )
    session.add(dish_1)
    session.commit()

    response = client.patch(
            f"/api/v1/menus/1/submenus/{dish_1.submenu_id}/dishes/{dish_1.id}",
            json={"title": "Update dish 1"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Update dish 1"
    assert data["description"] == "Dish description 1"
    assert data["price"] == "99.99"
    assert data["id"] == dish_1.id


def test_delete_dish(session: Session, client: TestClient):
    dish_1 = Dish(
        title="Dish 1",
        description="Dish description 1",
        price=99.99,
        submenu_id=1
    )
    session.add(dish_1)
    session.commit()

    response = client.delete(
            f"/api/v1/menus/1/submenus/{dish_1.submenu_id}/dishes/{dish_1.id}",
    )
    dish_in_db = session.get(Dish, dish_1.id)

    assert response.status_code == 200
    assert dish_in_db is None
