from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from app.models.base_model import BaseDBModel

class Admin(BaseDBModel):
    """
    管理员模型
    """
    __tablename__ = "admins"

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
    
    # 管理员特有字段
    role: Mapped[str] = mapped_column(
        String(20), 
        default="admin",
        comment="角色：admin, super_admin"
    )
    full_name: Mapped[str] = mapped_column(
        String(100),
        comment="全名"
    )
    phone_number: Mapped[str] = mapped_column(
        String(20), 
        nullable=True,
        comment="电话号码"
    )
    last_login: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=True,
        comment="最后登录时间"
    )

    def __repr__(self) -> str:
        return f"<Admin {self.username}>"