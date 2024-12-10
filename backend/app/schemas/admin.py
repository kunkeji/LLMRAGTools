from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Shared properties
class AdminBase(BaseModel):
    """管理员基础信息"""
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    username: Optional[str] = Field(None, description="用户名")
    is_active: Optional[bool] = Field(True, description="是否激活")
    role: Optional[str] = Field("admin", description="角色：admin=普通管理员, super_admin=超级管理员")
    full_name: Optional[str] = Field(None, description="全名")
    phone_number: Optional[str] = Field(None, description="电话号码")

# Properties to receive via API on creation
class AdminCreate(AdminBase):
    """管理员创建模型"""
    username: str = Field(..., description="用户名（必填）")
    email: EmailStr = Field(..., description="邮箱地址（必填）")
    password: str = Field(..., description="密码（必填）")
    full_name: str = Field(..., description="全名（必填）")
    role: str = Field("admin", description="角色（默认为普通管理员）")

# Properties to receive via API on update
class AdminUpdate(AdminBase):
    """管理员更新模型"""
    password: Optional[str] = Field(None, description="密码（可选）")

# Properties shared by models stored in DB
class AdminInDBBase(AdminBase):
    """数据库中的管理员基础模型"""
    id: Optional[int] = Field(None, description="管理员ID")
    last_login: Optional[datetime] = Field(None, description="最后登录时间")
    created_at: Optional[datetime] = Field(None, description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")

    class Config:
        from_attributes = True

# Additional properties to return via API
class Admin(AdminInDBBase):
    """API响应中的管理员模型"""
    pass

# Additional properties stored in DB
class AdminInDB(AdminInDBBase):
    """数据库中的完整管理员模型"""
    hashed_password: str = Field(..., description="密码哈希") 