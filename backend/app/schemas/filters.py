from datetime import datetime
from typing import Optional, List
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema

class DateRangeFilter(BaseSchema):
    """日期范围过滤"""
    start_date: Optional[datetime] = Field(None, description="开始日期")
    end_date: Optional[datetime] = Field(None, description="结束日期")

    @field_validator('end_date')
    def validate_date_range(cls, v: Optional[datetime], values: dict) -> Optional[datetime]:
        """验证日期范围"""
        if v and values.get('start_date') and v < values['start_date']:
            raise ValueError('结束日期不能早于开始日期')
        return v

class UserFilter(BaseSchema):
    """用户查询过滤"""
    keyword: Optional[str] = Field(None, min_length=1, max_length=50, description="关键词(用户名/邮箱/手机号)")
    status: Optional[str] = Field(None, description="状态")
    is_active: Optional[bool] = Field(None, description="是否激活")
    date_range: Optional[DateRangeFilter] = Field(None, description="日期范围")
    roles: Optional[List[str]] = Field(None, description="角色列表")

    @field_validator('status')
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        """验证状态"""
        if v is not None and v not in {'active', 'banned', 'pending'}:
            raise ValueError('无效的状态值')
        return v

class AdminFilter(BaseSchema):
    """管理员查询过滤"""
    keyword: Optional[str] = Field(None, min_length=1, max_length=50, description="关键词(用户名/邮箱/手机号)")
    role: Optional[str] = Field(None, description="角色")
    is_active: Optional[bool] = Field(None, description="是否激活")
    date_range: Optional[DateRangeFilter] = Field(None, description="日期范围")

    @field_validator('role')
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        """验证角色"""
        if v is not None and v not in {'admin', 'super_admin'}:
            raise ValueError('无效的角色值')
        return v

class LogFilter(BaseSchema):
    """日志查询过滤"""
    level: Optional[str] = Field(None, description="日志级别")
    module: Optional[str] = Field(None, description="模块名称")
    date_range: Optional[DateRangeFilter] = Field(None, description="日期范围")
    user_id: Optional[int] = Field(None, ge=1, description="用户ID")
    ip_address: Optional[str] = Field(None, description="IP地址")

    @field_validator('level')
    def validate_level(cls, v: Optional[str]) -> Optional[str]:
        """验证日志级别"""
        if v is not None and v not in {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}:
            raise ValueError('无效的日志级别')
        return v 