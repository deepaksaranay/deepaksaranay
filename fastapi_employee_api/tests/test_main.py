from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["message"] == "Employee Management API is running"


def test_employee_requires_authentication():
    with TestClient(app) as client:
        response = client.get("/employees")
        assert response.status_code == 401


def test_authentication_and_employee_crud():
    with TestClient(app) as client:
        username = "test_user_crud"
        password = "strongpassword123"

        register = client.post("/auth/register", json={"username": username, "password": password})
        assert register.status_code in (201, 409)

        login = client.post("/auth/login", json={"username": username, "password": password})
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        create = client.post(
            "/employees",
            headers=headers,
            json={
                "name": "Test Employee",
                "email": "test.employee@example.com",
                "department": "Engineering",
                "salary": 60000,
            },
        )
        assert create.status_code == 201
        employee_id = create.json()["id"]

        get_response = client.get(f"/employees/{employee_id}", headers=headers)
        assert get_response.status_code == 200

        update = client.put(
            f"/employees/{employee_id}",
            headers=headers,
            json={"salary": 70000},
        )
        assert update.status_code == 200
        assert update.json()["salary"] == 70000

        delete = client.delete(f"/employees/{employee_id}", headers=headers)
        assert delete.status_code == 200
