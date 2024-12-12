"""
邮箱提供商相关的Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import Field, field_validator
from app.schemas.base import BaseSchema

class EmailProviderBase(BaseSchema):
    """邮箱提供商基础Schema"""
    name: str = Field(..., min_length=2, max_length=100, description="提供商名称")
    domain_suffix: str = Field(..., min_length=1, max_length=100, description="域名后缀")
    smtp_host: str = Field(..., min_length=1, max_length=200, description="SMTP服务器地址")
    smtp_port: int = Field(..., gt=0, lt=65536, description="SMTP端口号")
    imap_host: str = Field(..., min_length=1, max_length=200, description="IMAP服务器地址")
    imap_port: int = Field(..., gt=0, lt=65536, description="IMAP端口号")
    use_ssl: bool = Field(default=True, description="是否使用SSL")
    use_tls: bool = Field(default=False, description="是否使用TLS")
    is_active: bool = Field(default=True, description="是否启用")
    logo_url: Optional[str] = Field(None, max_length=500, description="Logo URL")
    description: Optional[str] = Field(None, max_length=500, description="描述信息")
    help_url: Optional[str] = Field(None, max_length=500, description="帮助文档URL")
    auth_help_url: Optional[str] = Field(None, max_length=500, description="授权帮助URL")
    sort_order: int = Field(default=0, description="排序顺序")

    @field_validator('domain_suffix')
    def validate_domain_suffix(cls, v: str) -> str:
        """验证域名后缀格式"""
        if not v.startswith('@'):
            v = '@' + v
        return v

class EmailProviderCreate(EmailProviderBase):
    """创建邮箱提供商"""
    pass

class EmailProviderUpdate(BaseSchema):
    """更新邮箱提供商"""
    name: Optional[str] = Field(None, min_length=2, max_length=100, description="提供商名称")
    domain_suffix: Optional[str] = Field(None, min_length=1, max_length=100, description="域名后缀")
    smtp_host: Optional[str] = Field(None, min_length=1, max_length=200, description="SMTP服务器地址")
    smtp_port: Optional[int] = Field(None, gt=0, lt=65536, description="SMTP端口号")
    imap_host: Optional[str] = Field(None, min_length=1, max_length=200, description="IMAP服务器地址")
    imap_port: Optional[int] = Field(None, gt=0, lt=65536, description="IMAP端口号")
    use_ssl: Optional[bool] = Field(None, description="是否使用SSL")
    use_tls: Optional[bool] = Field(None, description="是否使用TLS")
    is_active: Optional[bool] = Field(None, description="是否启用")
    logo_url: Optional[str] = Field(None, max_length=500, description="Logo URL")
    description: Optional[str] = Field(None, max_length=500, description="描述信息")
    help_url: Optional[str] = Field(None, max_length=500, description="帮助文档URL")
    auth_help_url: Optional[str] = Field(None, max_length=500, description="授权帮助URL")
    sort_order: Optional[int] = Field(None, description="排序顺序")

    @field_validator('domain_suffix')
    def validate_domain_suffix(cls, v: Optional[str]) -> Optional[str]:
        """验证域名后缀格式"""
        if v and not v.startswith('@'):
            v = '@' + v
        return v

class EmailProviderInDBBase(EmailProviderBase):
    """数据库中的邮箱提供商基础信息"""
    id: int = Field(..., description="提供商ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    deleted_at: Optional[datetime] = Field(None, description="删除时间")

    class Config:
        from_attributes = True

class EmailProvider(EmailProviderInDBBase):
    """返回的邮箱提供商信息"""
    pass