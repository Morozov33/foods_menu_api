import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from menu_app.main import Menu


def test_create_menu(client: TestClient):
    response = client.post(
            "/api/v1/menus/",
            json={"title": "Menu 1", "description": "Menu description 1"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Menu 1"
    assert data["description"] == "Menu description 1"


def test_create_menu_incomplete(client: TestClient):
    # No description
    response = client.post("/api/v1/menus", json={"title": "Menu 1"})

    assert response.status_code == 422


def test_create_menu_invalid(client: TestClient):
    # title has an invalid type
    response = client.post(
        "/api/v1/menus",
        json={
            "title": {"message": "Menu 1"},
            "description": "Menu description 1",
        },
    )

    assert response.status_code == 422


def test_read_menus(session: Session, client: TestClient):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    menu_2 = Menu(title="Menu 2", description="Menu description 1")
    session.add(menu_1)
    session.add(menu_2)
    session.commit()

    response = client.get("/api/v1/menus")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == menu_1.title
    assert data[0]["description"] == menu_1.description
    assert data[0]["id"] == str(menu_1.id)
    assert data[1]["title"] == menu_2.title
    assert data[1]["description"] == menu_2.description
    assert data[1]["id"] == str(menu_2.id)


def test_read_menu(session: Session, client: TestClient):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    session.add(menu_1)
    session.commit()

    response = client.get(f"/api/v1/menus/{menu_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == menu_1.title
    assert data["description"] == menu_1.description
    assert data["id"] == str(menu_1.id)


def test_update_menu(session: Session, client: TestClient):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    session.add(menu_1)
    session.commit()

    response = client.patch(
            f"/api/v1/menus/{menu_1.id}",
            json={"title": "Update menu 1"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Update menu 1"
    assert data["description"] == "Menu description 1"
    assert data["id"] == str(menu_1.id)


def test_delete_menu(session: Session, client: TestClient):
    menu_1 = Menu(title="Menu 1", description="Menu description 1")
    session.add(menu_1)
    session.commit()

    response = client.delete(f"/api/v1/menus/{menu_1.id}")
    menu_in_db = session.get(Menu, menu_1.id)

    assert response.status_code == 200
    assert menu_in_db is None
