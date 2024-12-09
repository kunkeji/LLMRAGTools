from typing import Dict
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.tests.utils.admin import create_random_admin
from app.tests.utils.utils import random_email, random_lower_string

def test_admin_login(client: TestClient, db: Session) -> None:
    """测试管理员登录"""
    login_data = {
        "username": random_lower_string(),
        "password": random_lower_string(),
    }
    admin = create_random_admin(db, login_data)
    response = client.post(f"{settings.API_V1_STR}/admin/login", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]

def test_admin_me(client: TestClient, admin_token_headers: Dict[str, str]) -> None:
    """测试获取当前管理员信息"""
    response = client.get(
        f"{settings.API_V1_STR}/admin/me", headers=admin_token_headers,
    )
    result = response.json()
    assert response.status_code == 200
    assert "username" in result
    assert "email" in result

def test_create_admin_by_super_admin(
    client: TestClient, super_admin_token_headers: Dict[str, str], db: Session
) -> None:
    """测试超级管理员创建管理员"""
    data = {
        "username": random_lower_string(),
        "email": random_email(),
        "password": random_lower_string(),
        "full_name": random_lower_string(),
        "role": "admin"
    }
    response = client.post(
        f"{settings.API_V1_STR}/admin/create-admin",
        headers=super_admin_token_headers,
        json=data,
    )
    result = response.json()
    assert response.status_code == 200
    assert result["email"] == data["email"]
    assert result["username"] == data["username"]
    assert result["role"] == "admin"

def test_create_admin_by_normal_admin(
    client: TestClient, admin_token_headers: Dict[str, str], db: Session
) -> None:
    """测试普通管理员创建管理员（应该失败）"""
    data = {
        "username": random_lower_string(),
        "email": random_email(),
        "password": random_lower_string(),
        "full_name": random_lower_string(),
        "role": "admin"
    }
    response = client.post(
        f"{settings.API_V1_STR}/admin/create-admin",
        headers=admin_token_headers,
        json=data,
    )
    assert response.status_code == 403
    assert "权限不足" in response.json()["detail"] 