from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str  # 用户ID或管理员ID
    exp: int  # 过期时间
    type: str  # token类型：user, admin
    role: Optional[str] = None  # 角色：user, admin, super_admin
    status: Optional[str] = None  # 用户状态