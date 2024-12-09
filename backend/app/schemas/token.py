from typing import Optional, Dict, Any
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: Optional[str] = None  # 用户ID或管理员ID
    role: Optional[str] = None  # 用户角色：user, admin, super_admin
    exp: Optional[int] = None  # 过期时间
    type: Optional[str] = None  # token类型：user, admin