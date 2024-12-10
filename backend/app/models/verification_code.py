from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, Boolean
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

    def is_valid(self) -> bool:
        """
        验证码是否有效
        """
        return not self.is_used and datetime.utcnow() <= self.expires_at 