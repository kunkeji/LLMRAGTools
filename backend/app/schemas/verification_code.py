from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# 验证码用途枚举
VerificationPurpose = Literal["register", "reset_password"]

class VerificationCodeBase(BaseModel):
    """验证码基础模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    purpose: VerificationPurpose = Field(default="register", description="验证码用途")

class VerificationCodeCreate(VerificationCodeBase):
    """创建验证码请求模型"""
    pass

class VerificationCodeVerify(BaseModel):
    """验证码验证请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    purpose: VerificationPurpose = Field(default="register", description="验证码用途")

class ResetPasswordRequest(BaseModel):
    """重置密码请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, description="验证码")
    new_password: str = Field(..., min_length=6, description="新密码")
    purpose: Literal["reset_password"] = Field(default="reset_password", description="验证码用途")

class VerificationCode(VerificationCodeBase):
    """验证码响应模型"""
    id: int
    code: str
    expires_at: datetime
    is_used: bool
    created_at: datetime

    class Config:
        from_attributes = True