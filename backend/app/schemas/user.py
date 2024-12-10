from typing import Optional
from datetime import datetime
from pydantic import EmailStr, Field, field_validator
from app.schemas.base import BaseSchema

class UserBase(BaseSchema):
    """用户基础信息"""
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    username: Optional[str] = Field(None, min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$", description="用户名")
    is_active: Optional[bool] = Field(True, description="是否激活")
    nickname: Optional[str] = Field(None, min_length=2, max_length=20, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    phone_number: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="电话号码")
    status: Optional[str] = Field("active", description="状态：active=正常, banned=禁用")

    @field_validator('username')
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """验证用户名"""
        if v is None:
            return v
        if len(v) < 3 or len(v) > 20:
            raise ValueError('用户名长度必须在3-20个字符之间')
        if not v.isalnum() and not all(c in '_-' for c in v if not c.isalnum()):
            raise ValueError('用户名只能包含字母、数字、下划线和连字符')
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        """验证手机号码"""
        if v is None:
            return v
        if not v.isdigit() or len(v) != 11 or not v.startswith('1'):
            raise ValueError('无效的手机号码格式')
        return v

    @field_validator('status')
    def validate_status(cls, v: str) -> str:
        """验证状态"""
        valid_statuses = {'active', 'banned'}
        if v not in valid_statuses:
            raise ValueError('无效的状态值')
        return v

class UserCreate(BaseSchema):
    """用户创建模型"""
    email: EmailStr = Field(..., description="邮箱地址（必填）")
    username: str = Field(..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_-]+$", description="用户名（必填）")
    password: str = Field(..., min_length=6, max_length=32, description="密码（必填）")
    verification_code: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$", description="验证码（必填）")
    nickname: Optional[str] = Field(None, min_length=2, max_length=20, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    phone_number: Optional[str] = Field(None, pattern=r"^1[3-9]\d{9}$", description="电话号码")

    @field_validator('password')
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

class UserUpdate(UserBase):
    """用户更新模型"""
    password: Optional[str] = Field(None, min_length=6, max_length=32, description="密码（可选）")

    @field_validator('password')
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        """验证密码强度"""
        if v is None:
            return v
        if len(v) < 6:
            raise ValueError('密码长度不能小于6个字符')
        if len(v) > 32:
            raise ValueError('密码长度不能超过32个字符')
        # if not any(c.islower() for c in v):
        #     raise ValueError('密码必须包含至少一个小写字母')
        # if not any(c.isdigit() for c in v):
        #     raise ValueError('密码必须包含至少一个数字')
        return v

class UserInDBBase(UserBase):
    """数据库中的用户基础模型"""
    id: int = Field(..., description="用户ID")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class User(UserInDBBase):
    """API响应中的用户模型"""
    pass

class UserInDB(UserInDBBase):
    """数据库中的完整用户模型"""
    hashed_password: str = Field(..., description="密码哈希") 