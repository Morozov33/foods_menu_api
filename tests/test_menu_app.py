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
            json={"title": "Menu 1", "description": "My menu description 1"},
    )
    app.dependency_overrides.clear()
    data = response.json()

    assert response.status_code == 201
    assert data["title"] == "Menu 1"
    assert data["description"] == "My menu description 1"
