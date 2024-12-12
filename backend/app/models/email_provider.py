"""
邮箱提供商模型（作为模板使用）
"""
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer
from app.models.base_model import BaseDBModel

class EmailProvider(BaseDBModel):
    """邮箱提供商信息（预设模板）"""
    __tablename__ = "email_providers"

    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False,
        unique=True,
        index=True,
        comment="提供商名称"
    )
    logo_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="Logo URL"
    )
    domain_suffix: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="域名后缀（如 @qq.com）"
    )
    smtp_host: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="SMTP服务器地址"
    )
    smtp_port: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="SMTP端口号"
    )
    imap_host: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="IMAP服务器地址"
    )
    imap_port: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="IMAP端口号"
    )
    use_ssl: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="是否使用SSL"
    )
    use_tls: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="是否使用TLS"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="是否启用"
    )
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="描述信息"
    )
    help_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="帮助文档URL"
    )
    auth_help_url: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="授权帮助URL"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="排序顺序"
    )

    def __repr__(self) -> str:
        return f"<EmailProvider {self.name}>" 