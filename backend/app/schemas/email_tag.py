"""
邮件标签相关的Schema
"""
from datetime import datetime
from typing import Optional, List
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema

class EmailTagBase(BaseSchema):
    """标签基础Schema"""
    name: str = Field(..., min_length=1, max_length=50, description="标签名称")
    color: str = Field(default="#1890ff", pattern="^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", description="标签颜色(十六进制，支持3位或6位)")
    description: Optional[str] = Field(None, max_length=200, description="标签描述")
    sort_order: int = Field(default=0, description="排序顺序")

    @field_validator('color')
    def validate_color(cls, v: str) -> str:
        """验证颜色格式"""
        if not v.startswith('#'):
            v = f"#{v}"
        # 将3位颜色代码转换为6位
        if len(v) == 4:  # 包含#号的3位颜色
            v = '#' + ''.join(c + c for c in v[1:])
        return v.lower()

class EmailTagCreate(EmailTagBase):
    """创建标签Schema"""
    pass

class EmailTagUpdate(BaseSchema):
    """更新标签Schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="标签名称")
    color: Optional[str] = Field(None, pattern="^#[0-9a-fA-F]{6}$", description="标签颜色(十六进制)")
    description: Optional[str] = Field(None, max_length=200, description="标签描述")
    sort_order: Optional[int] = Field(None, description="排序顺序")

    @field_validator('color')
    def validate_color(cls, v: Optional[str]) -> Optional[str]:
        """验证颜色格式"""
        if v:
            if not v.startswith('#'):
                v = f"#{v}"
            return v.lower()
        return v

class EmailTag(EmailTagBase):
    """标签返回Schema"""
    id: int = Field(..., description="标签ID")
    user_id: Optional[int] = Field(None, description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

class EmailTagWithStats(EmailTag):
    """带统计信息的标签Schema"""
    email_count: int = Field(default=0, description="使用该标签的邮件数量") 