from typing import Dict, Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base
from app.main import app
from app.api.v1.deps.auth import get_db
from app.tests.utils.user import create_random_user
from app.tests.utils.admin import create_random_admin
from app.tests.utils.utils import (
    get_admin_token_headers,
    get_user_token_headers,
    random_email,
    random_lower_string,
)

# 使用测试数据库
SQLALCHEMY_TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/agent_db", "/test_agent_db"
)

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db() -> Generator:
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client() -> Generator:
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}

@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    """普通用户Token"""
    user = create_random_user(db)
    return get_user_token_headers(client, user.email, "password")

@pytest.fixture(scope="module")
def admin_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    """普通管理员Token"""
    admin = create_random_admin(db)
    return get_admin_token_headers(client, admin.username, "password")

@pytest.fixture(scope="module")
def super_admin_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    """超级管理员Token"""
    admin = create_random_admin(db, is_super=True)
    return get_admin_token_headers(client, admin.username, "password")
