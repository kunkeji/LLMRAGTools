from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_admin(client: TestClient, db: Session) -> None:
    data = {
        "email": "admin@example.com",
        "password": "admin123456",
        "username": "admin",
        "role": "admin",
        "full_name": "Test Admin"
    }
    response = client.post(
        f"/api/admin/create-admin",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert content["username"] == data["username"]
    assert content["role"] == data["role"]
    assert "id" in content

def test_admin_login(client: TestClient, db: Session) -> None:
    login_data = {
        "username": "admin",
        "password": "admin123456",
    }
    response = client.post(f"/api/admin/login", data=login_data)
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer"

def test_get_admin_me(client: TestClient, admin_token_headers: dict) -> None:
    response = client.get(f"/api/admin/me", headers=admin_token_headers)
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == "admin@example.com"
    assert content["username"] == "admin"
    assert content["role"] == "admin" 