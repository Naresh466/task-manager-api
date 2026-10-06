from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_task():
    response = client.post("/tasks", json={"title": "Write tests"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Write tests"
    assert data["status"] == "todo"
    assert data["id"] == 1


def test_list_tasks():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_missing_task_returns_404():
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task_status():
    client.post("/tasks", json={"title": "Finish project"})
    response = client.put("/tasks/1", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["title"] == "Finish project"


def test_delete_task():
    client.post("/tasks", json={"title": "Temporary"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert client.get("/tasks/1").status_code == 404