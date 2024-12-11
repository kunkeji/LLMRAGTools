"""
日志相关的Schema
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import Field
from app.schemas.base import BaseSchema
from app.models.log import LogLevel, LogType

class LogBase(BaseSchema):
    """日志基础Schema"""
    level: LogLevel = Field(..., description="日志级别")
    type: LogType = Field(..., description="日志类型")
    module: str = Field(..., description="模块名称")
    message: str = Field(..., description="日志消息")
    
    request_id: Optional[str] = Field(None, description="请求ID")
    method: Optional[str] = Field(None, description="HTTP方法")
    url: Optional[str] = Field(None, description="请求URL")
    ip_address: Optional[str] = Field(None, description="IP地址")
    user_agent: Optional[str] = Field(None, description="用户代理")
    
    user_id: Optional[int] = Field(None, description="用户ID")
    username: Optional[str] = Field(None, description="用户名")
    
    function: Optional[str] = Field(None, description="函数名称")
    details: Optional[Dict[str, Any]] = Field(None, description="详细信息")
    
    error_type: Optional[str] = Field(None, description="错误类型")
    error_stack: Optional[str] = Field(None, description="错误堆栈")
    
    duration: Optional[int] = Field(None, description="执行时长(毫秒)")

class LogCreate(LogBase):
    """创建日志"""
    pass

class LogInDB(LogBase):
    """数据库中的日志"""
    id: int = Field(..., description="日志ID")
    timestamp: datetime = Field(..., description="记录时间")

    class Config:
        from_attributes = True

class LogFilter(BaseSchema):
    """日志查询过滤"""
    level: Optional[LogLevel] = Field(None, description="日志级别")
    type: Optional[LogType] = Field(None, description="日志类型")
    start_time: Optional[datetime] = Field(None, description="开始时间")
    end_time: Optional[datetime] = Field(None, description="结束时间")
    user_id: Optional[int] = Field(None, description="用户ID")
    request_id: Optional[str] = Field(None, description="请求ID")
    module: Optional[str] = Field(None, description="模块名称")
    keyword: Optional[str] = Field(None, description="关键词搜索") 