"""
验证码模型
"""
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from datetime import datetime
from app.models.base_model import BaseDBModel

class VerificationCode(BaseDBModel):
    """
    验证码模型
    """
    __tablename__ = "verification_codes"

    email: Mapped[str] = mapped_column(
        String(255), 
        index=True,
        comment="邮箱"
    )
    code: Mapped[str] = mapped_column(
        String(6),
        comment="验证码"
    )
    purpose: Mapped[str] = mapped_column(
        String(20),
        comment="用途：register, reset_password"
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        comment="过期时间"
    )
    is_used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="是否已使用"
    )

    # 添加用户外键关联
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,  # 注册时可能还没有用户ID
        index=True,
        comment="用户ID"
    )
    
    # 添加与User模型的关系
    user = relationship(
        "User",
        back_populates="verification_codes",
        lazy="select"
    )

    def is_valid(self) -> bool:
        """
        验证码是否有效
        """
        return not self.is_used and datetime.utcnow() <= self.expires_at 