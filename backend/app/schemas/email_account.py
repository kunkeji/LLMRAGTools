"""
邮箱账户相关的Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import Field, field_validator, EmailStr
from app.schemas.base import BaseSchema
from app.models.email_account import SyncStatus

class EmailAccountBase(BaseSchema):
    """邮箱账户基础Schema"""
    email_address: EmailStr = Field(..., description="邮箱地址")
    display_name: Optional[str] = Field(None, max_length=100, description="显示名称")
    is_default: bool = Field(default=False, description="是否默认邮箱")
    is_active: bool = Field(default=True, description="是否启用")


    
    # 服务器配置
    smtp_host: str = Field(..., min_length=1, max_length=200, description="SMTP服务器地址")
    smtp_port: int = Field(..., gt=0, lt=65536, description="SMTP端口号")
    imap_host: str = Field(..., min_length=1, max_length=200, description="IMAP服务器地址")
    imap_port: int = Field(..., gt=0, lt=65536, description="IMAP端口号")
    use_ssl: bool = Field(default=True, description="是否使用SSL")
    use_tls: bool = Field(default=False, description="是否使用TLS")

    # 服务器测试
    smtp_last_test_time: Optional[datetime] = Field(None, description="SMTP最后测试时间")
    smtp_test_result: Optional[bool] = Field(None, description="SMTP测试结果")
    smtp_test_error: Optional[str] = Field(None, description="SMTP测试错误信息")
    imap_last_test_time: Optional[datetime] = Field(None, description="IMAP最后测试时间")
    imap_test_result: Optional[bool] = Field(None, description="IMAP测试结果")
    imap_test_error: Optional[str] = Field(None, description="IMAP测试错误信息")
    
    # 自定义配置
    sync_interval: int = Field(default=30, ge=1, le=1440, description="同步间隔(分钟)")
    keep_days: int = Field(default=30, ge=1, le=365, description="邮件保留天数")

class EmailAccountCreate(EmailAccountBase):
    """创建邮箱账户"""
    auth_token: str = Field(..., min_length=1, max_length=500, description="授权码/密码")

class EmailAccountUpdate(BaseSchema):
    """更新邮箱账户"""
    email_address: Optional[EmailStr] = Field(None, description="邮箱地址")
    display_name: Optional[str] = Field(None, max_length=100, description="显示名称")
    is_default: Optional[bool] = Field(None, description="是否默认邮箱")
    is_active: Optional[bool] = Field(None, description="是否启用")
    auth_token: Optional[str] = Field(None, min_length=1, max_length=500, description="授权码/密码")
    
    # 服务器配置
    smtp_host: Optional[str] = Field(None, min_length=1, max_length=200, description="SMTP服务器地址")
    smtp_port: Optional[int] = Field(None, gt=0, lt=65536, description="SMTP端口号")
    imap_host: Optional[str] = Field(None, min_length=1, max_length=200, description="IMAP服务器地址")
    imap_port: Optional[int] = Field(None, gt=0, lt=65536, description="IMAP端口号")
    use_ssl: Optional[bool] = Field(None, description="是否使用SSL")
    use_tls: Optional[bool] = Field(None, description="是否使用TLS")
    
    # 自定义配置
    sync_interval: Optional[int] = Field(None, ge=1, le=1440, description="同步间隔(分钟)")
    keep_days: Optional[int] = Field(None, ge=1, le=365, description="邮件保留天数")

class EmailAccountInDBBase(EmailAccountBase):
    """数据库中的邮箱账户基础信息"""
    id: int = Field(..., description="账户ID")
    user_id: int = Field(..., description="用户ID")
    auth_token: str = Field(..., description="授权码/密码")
    sync_status: SyncStatus = Field(default=SyncStatus.NEVER, description="同步状态")
    last_sync_time: Optional[datetime] = Field(None, description="最后同步时间")
    next_sync_time: Optional[datetime] = Field(None, description="下次同步时间")
    sync_error: Optional[str] = Field(None, description="同步错误信息")
    total_emails: int = Field(default=0, description="总邮件数")
    unread_emails: int = Field(default=0, description="未读邮件数")
    last_email_time: Optional[datetime] = Field(None, description="最新邮件时间")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    
    # 服务器测试相关字段
    smtp_last_test_time: Optional[datetime] = Field(None, description="SMTP最后测试时间")
    smtp_test_result: Optional[bool] = Field(None, description="SMTP测试结果")
    smtp_test_error: Optional[str] = Field(None, description="SMTP测试错误信息")
    imap_last_test_time: Optional[datetime] = Field(None, description="IMAP最后测试时间")
    imap_test_result: Optional[bool] = Field(None, description="IMAP测试结果")
    imap_test_error: Optional[str] = Field(None, description="IMAP测试错误信息")

    @field_validator('sync_status', mode='before')
    def validate_sync_status(cls, v: str) -> SyncStatus:
        """验证并转换同步状态"""
        if isinstance(v, str):
            try:
                return SyncStatus[v.upper()]
            except KeyError:
                raise ValueError(f"Invalid sync status: {v}")
        return v

    class Config:
        from_attributes = True
        use_enum_values = True

class EmailAccountResponse(EmailAccountInDBBase):
    """返回给API的邮箱账户信息"""
    smtp_last_test_time: Optional[datetime] = None
    smtp_test_result: Optional[bool] = None
    smtp_test_error: Optional[str] = None
    imap_last_test_time: Optional[datetime] = None
    imap_test_result: Optional[bool] = None
    imap_test_error: Optional[str] = None

    class Config:
        from_attributes = True
        use_enum_values = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "email_address": "example@qq.com",
                "display_name": "我的QQ邮箱",
                "auth_token": "abcdefghijklmn",
                "is_default": True,
                "is_active": True,
                "smtp_host": "smtp.qq.com",
                "smtp_port": 465,
                "imap_host": "imap.qq.com",
                "imap_port": 993,
                "use_ssl": True,
                "use_tls": False,
                "sync_status": "never",
                "last_sync_time": None,
                "next_sync_time": None,
                "sync_error": None,
                "total_emails": 0,
                "unread_emails": 0,
                "last_email_time": None,
                "sync_interval": 30,
                "keep_days": 30,
                "smtp_last_test_time": "2024-01-20T08:30:00Z",
                "smtp_test_result": True,
                "smtp_test_error": None,
                "imap_last_test_time": "2024-01-20T08:30:00Z",
                "imap_test_result": True,
                "imap_test_error": None,
                "created_at": "2024-01-20T08:30:00Z",
                "updated_at": "2024-01-20T08:30:00Z"
            }
        }

class EmailAccountWithStats(EmailAccountResponse):
    """带统计信息的邮箱账户"""
    pass 