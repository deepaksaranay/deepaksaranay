from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Employee Management API is running"


def test_create_employee():
    response = client.post(
        "/employees",
        json={
            "name": "Test Employee",
            "email": "test.employee@example.com",
            "department": "Engineering",
            "salary": 60000,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Employee"
    assert "id" in data
