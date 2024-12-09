from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from app.models.base_model import BaseDBModel

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

    def __repr__(self) -> str:
        return f"<User {self.username}>"