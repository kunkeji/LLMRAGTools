import random
import string
from typing import Dict

def random_lower_string(length: int = 32) -> str:
    """生成随机小写字符串"""
    return "".join(random.choices(string.ascii_lowercase, k=length))

def random_email() -> str:
    """生成随机邮箱"""
    return f"{random_lower_string(10)}@{random_lower_string(6)}.com"

def random_phone() -> str:
    """生成随机手机号"""
    return f"1{''.join(random.choices(string.digits, k=10))}"

def get_admin_token_headers(client, email: str, password: str) -> Dict[str, str]:
    """获取管理员认证头"""
    data = {"username": email, "password": password}
    r = client.post("/api/admin/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def get_user_token_headers(client, email: str, password: str) -> Dict[str, str]:
    """获取用户认证头"""
    data = {"username": email, "password": password}
    r = client.post("/api/user/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers 