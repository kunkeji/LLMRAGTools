"""
用户邮箱账户模型
"""
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Enum as SQLEnum
from enum import Enum
from app.models.base_model import BaseDBModel

class SyncStatus(str, Enum):
    """同步状态"""
    NEVER = "NEVER"         # 从未同步
    SYNCING = "SYNCING"     # 同步中
    SUCCESS = "SUCCESS"     # 同步成功
    FAILED = "FAILED"       # 同步失败
    ERROR = "ERROR"         # 同步错误

class EmailAccount(BaseDBModel):
    """用户邮箱账户信息"""
    __tablename__ = "email_accounts"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    email_address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="邮箱地址"
    )
    auth_token: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="授权码/密码"
    )
    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
        comment="显示名称"
    )
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="是否默认邮箱"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        comment="是否启用"
    )
    
    # 服务器配置
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
    
    # 同步相关字段
    sync_status: Mapped[str] = mapped_column(
        SQLEnum(SyncStatus),
        default=SyncStatus.NEVER,
        comment="同步状态"
    )
    last_sync_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="最后同步时间"
    )
    next_sync_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="下次同步时间"
    )
    sync_error: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="同步错误信息"
    )
    
    # 统计信息
    total_emails: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="总邮件数"
    )
    unread_emails: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="未读邮件数"
    )
    last_email_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="最新邮件时间"
    )
    
    # 自定义配置
    sync_interval: Mapped[int] = mapped_column(
        Integer,
        default=30,
        comment="同步间隔(分钟)"
    )
    keep_days: Mapped[int] = mapped_column(
        Integer,
        default=30,
        comment="邮件保留天数"
    )
    
    # 服务器测试相关字段
    smtp_last_test_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="SMTP最后测试时间"
    )
    smtp_test_result: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        comment="SMTP测试结果"
    )
    smtp_test_error: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="SMTP测试错误信息"
    )
    imap_last_test_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        comment="IMAP最后测试时间"
    )
    imap_test_result: Mapped[bool] = mapped_column(
        Boolean,
        nullable=True,
        comment="IMAP测试结果"
    )
    imap_test_error: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="IMAP测试错误信息"
    )
    
    # 关联关系
    user = relationship("User", back_populates="email_accounts")

    def __repr__(self) -> str:
        return f"<EmailAccount {self.email_address}>"