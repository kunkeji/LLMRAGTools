from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string

def test_get_access_token(client: TestClient, db: Session) -> None:
    """测试获取访问令牌"""
    login_data = {
        "username": random_email(),
        "password": random_lower_string(),
    }
    user = create_random_user(db, login_data)
    response = client.post(f"{settings.API_V1_STR}/user/login", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_use_access_token(client: TestClient, normal_user_token_headers: Dict[str, str]) -> None:
    """测试使用访问令牌"""
    response = client.post(
        f"{settings.API_V1_STR}/user/test-token", headers=normal_user_token_headers,
    )
    result = response.json()
    assert response.status_code == 200
    assert "email" in result

def test_register_user(client: TestClient, db: Session) -> None:
    """测试用户注册"""
    data = {
        "email": random_email(),
        "password": random_lower_string(),
        "first_name": random_lower_string(),
        "last_name": random_lower_string(),
    }
    response = client.post(f"{settings.API_V1_STR}/user/register", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["email"] == data["email"]
    assert "id" in result

def test_register_existing_user(client: TestClient, db: Session) -> None:
    """测试注册已存在的用户"""
    email = random_email()
    password = random_lower_string()
    user = create_random_user(db, {"username": email, "password": password})
    
    data = {
        "email": email,
        "password": password,
        "first_name": random_lower_string(),
        "last_name": random_lower_string(),
    }
    response = client.post(f"{settings.API_V1_STR}/user/register", json=data)
    assert response.status_code == 400
    assert "该邮箱已被注册" in response.json()["detail"] 