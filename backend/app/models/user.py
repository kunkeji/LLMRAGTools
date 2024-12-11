from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from app.models.base_model import BaseDBModel
from sqlalchemy.orm import relationship

class User(BaseDBModel):
    """
    用户模型
    """
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50), 
        unique=True, 
        index=True,
        comment="用户名"
    )
    email: Mapped[str] = mapped_column(
        String(255), 
        unique=True, 
        index=True,
        comment="邮箱"
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        comment="密码哈希"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True,
        comment="是否激活"
    )
    
    # 用户特有字段
    nickname: Mapped[str] = mapped_column(
        String(50), 
        nullable=True,
        comment="昵称"
    )
    avatar: Mapped[str] = mapped_column(
        String(255), 
        nullable=True,
        comment="头像"
    )
    phone_number: Mapped[str] = mapped_column(
        String(20), 
        nullable=True,
        comment="电话号码"
    )
    
    # 状态跟踪
    status: Mapped[str] = mapped_column(
        String(20), 
        default="active",
        comment="状态：active, banned, etc."
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=True,
        comment="最后登录时间"
    )

    # 关联关系
    verification_codes = relationship("VerificationCode", back_populates="user")
    llm_channels = relationship("LLMChannel", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def to_dict(self) -> dict:
        """
        转换为字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "nickname": self.nickname or self.username,
            "avatar": self.avatar,
            "phone_number": self.phone_number,
            "status": self.status,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }