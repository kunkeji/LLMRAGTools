from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_user(client: TestClient, db: Session) -> None:
    data = {
        "email": "test@example.com",
        "password": "test123456",
        "username": "testuser",
        "nickname": "Test User"
    }
    response = client.post(
        f"/api/user/register",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["email"] == data["email"]
    assert content["username"] == data["username"]
    assert "id" in content

def test_user_login(client: TestClient, db: Session) -> None:
    login_data = {
        "username": "test@example.com",  # 使用邮箱作为登录名
        "password": "test123456",
    }
    response = client.post(f"/api/user/login", data=login_data)
    assert response.status_code == 200
    content = response.json()
    assert "access_token" in content
    assert content["token_type"] == "bearer" 