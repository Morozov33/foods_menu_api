from fastapi.testclient import TestClient
from sqlmodel import Session
from menu_app.main import Submenu


def test_create_submenu(client: TestClient):
    response = client.post(
                "/api/v1/menus/1/submenus",
                json={"title": "Submenu 1",
                      "description": "Submenu description 1"},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Submenu 1"
    assert data["description"] == "Submenu description 1"
    assert data["menu_id"] == 1


def test_create_submenu_incomplete(client: TestClient):
    # No description
    response = client.post("/api/v1/menus/1/submenus",
                           json={"title": "Menu 1"})

    assert response.status_code == 422


def test_create_submenu_invalid(client: TestClient):
    # title has an invalid type
    response = client.post(
        "/api/v1/menus/1/submenus",
        json={
            "title": {"message": "Submenu 1"},
            "description": "Submenu description 1",
        },
    )

    assert response.status_code == 422


def test_read_submenus(session: Session, client: TestClient):
    submenu_1 = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=1
    )
    submenu_2 = Submenu(
            title="Submenu 2",
            description="Submenu description 1",
            menu_id=1
    )
    session.add(submenu_1)
    session.add(submenu_2)
    session.commit()

    response = client.get(f"/api/v1/menus/{submenu_1.menu_id}/submenus")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == submenu_1.title
    assert data[0]["description"] == submenu_1.description
    assert data[0]["id"] == str(submenu_1.id)
    assert data[0]["menu_id"] == submenu_1.menu_id
    assert data[1]["title"] == submenu_2.title
    assert data[1]["description"] == submenu_2.description
    assert data[1]["id"] == str(submenu_2.id)
    assert data[1]["menu_id"] == submenu_2.menu_id


def test_read_submenu(session: Session, client: TestClient):
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=1
    )
    session.add(submenu)
    session.commit()

    response = client.get(
            f"/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}"
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == submenu.title
    assert data["description"] == submenu.description
    assert data["id"] == str(submenu.id)
    assert data["menu_id"] == submenu.menu_id


def test_update_submenu(session: Session, client: TestClient):
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=1
    )
    session.add(submenu)
    session.commit()

    response = client.patch(
            f"/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}",
            json={"title": "Update submenu 1"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["title"] == "Update submenu 1"
    assert data["description"] == "Submenu description 1"
    assert data["id"] == submenu.id


def test_delete_menu(session: Session, client: TestClient):
    submenu = Submenu(
            title="Submenu 1",
            description="Submenu description 1",
            menu_id=1
    )
    session.add(submenu)
    session.commit()

    response = client.delete(
            f"/api/v1/menus/{submenu.menu_id}/submenus/{submenu.id}"
    )
    submenu_in_db = session.get(Submenu, submenu.id)

    assert response.status_code == 200
    assert submenu_in_db is None
