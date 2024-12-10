from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    """用户基础信息"""
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    username: Optional[str] = Field(None, description="用户名")
    is_active: Optional[bool] = Field(True, description="是否激活")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    phone_number: Optional[str] = Field(None, description="电话号码")
    status: Optional[str] = Field("active", description="状态：active=正常, banned=禁用")

# Properties to receive via API on creation
class UserCreate(BaseModel):
    """用户创建模型"""
    email: EmailStr = Field(..., description="邮箱地址（必填）")
    username: str = Field(..., description="用户名（必填）")
    password: str = Field(..., description="密码（必填）")
    verification_code: str = Field(..., description="验证码（必填）")
    nickname: Optional[str] = Field(None, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    phone_number: Optional[str] = Field(None, description="电话号码")
    status: Optional[str] = Field("active", description="状态")

# Properties to receive via API on update
class UserUpdate(UserBase):
    """用户更新模型"""
    password: Optional[str] = Field(None, description="密码（可选）")

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    """数据库中的用户基础模型"""
    id: int = Field(..., description="用户ID")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

# Additional properties to return via API
class User(UserInDBBase):
    """API响应中的用户模型"""
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    """数据库中的完整用户模型"""
    hashed_password: str = Field(..., description="密码哈希") 