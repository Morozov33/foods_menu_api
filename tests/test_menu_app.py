import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from menu_app.main import app, get_session, Menu, Submenu, Dish


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_menu(client: TestClient):
    response = client.post(
            "/api/v1/menus/",
            json={"title": "Menu 1", "description": "Menu description 1"},
    )
    app.dependency_overrides.clear()
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
