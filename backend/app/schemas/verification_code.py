from typing import Literal
from datetime import datetime
from pydantic import EmailStr, Field, field_validator
from app.schemas.base import BaseSchema

# 验证码用途枚举
VerificationPurpose = Literal["register", "reset_password"]

class VerificationCodeBase(BaseSchema):
    """验证码基础模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    purpose: VerificationPurpose = Field(default="register", description="验证码用途")

    @field_validator('purpose')
    def validate_purpose(cls, v: str) -> str:
        """验证用途"""
        valid_purposes = {'register', 'reset_password'}
        if v not in valid_purposes:
            raise ValueError('无效的验证码用途')
        return v

class VerificationCodeCreate(VerificationCodeBase):
    """创建验证码请求模型"""
    pass

class VerificationCodeVerify(BaseSchema):
    """验证码验证请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$", description="验证码")
    purpose: VerificationPurpose = Field(default="register", description="验证码用途")

    @field_validator('code')
    def validate_code(cls, v: str) -> str:
        """验证验证码格式"""
        if not v.isdigit():
            raise ValueError('验证码必须是6位数字')
        return v

class ResetPasswordRequest(BaseSchema):
    """重置密码请求模型"""
    email: EmailStr = Field(..., description="邮箱地址")
    code: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$", description="验证码")
    new_password: str = Field(..., min_length=6, max_length=32, description="新密码")
    purpose: Literal["reset_password"] = Field(default="reset_password", description="验证码用途")

    @field_validator('new_password')
    def validate_password(cls, v: str) -> str:
        """验证密码强度"""
        if len(v) < 6:
            raise ValueError('密码长度不能小于6个字符')
        if len(v) > 32:
            raise ValueError('密码长度不能超过32个字符')
        # if not any(c.isupper() for c in v):
        #     raise ValueError('密码必须包含至少一个大写字母')
        # if not any(c.islower() for c in v):
        #     raise ValueError('密码必须包含至少一个小写字母')
        # if not any(c.isdigit() for c in v):
        #     raise ValueError('密码必须包含至少一个数字')
        return v

class VerificationCode(VerificationCodeBase):
    """验证码响应模型"""
    id: int = Field(..., description="验证码ID")
    code: str = Field(..., description="验证码")
    expires_at: datetime = Field(..., description="过期时间")
    is_used: bool = Field(..., description="是否已使用")
    created_at: datetime = Field(..., description="创建时间")