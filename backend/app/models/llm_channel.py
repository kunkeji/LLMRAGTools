"""
LLM模型渠道管理模型
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models.base_model import BaseDBModel

class LLMChannel(BaseDBModel):
    """LLM模型渠道信息"""
    __tablename__ = "llm_channels"

    user_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    channel_name: str = Column(
        String(100),
        nullable=False,
        comment="渠道名称"
    )
    model_type: str = Column(
        String(50),
        nullable=False,
        comment="模型类型"
    )
    model: str = Column(
        String(50),
        nullable=False,
        comment="具体模型"
    )
    api_key: str = Column(
        String(500),
        nullable=False,
        comment="API密钥"
    )
    proxy_url: str = Column(
        String(200),
        nullable=True,
        comment="代理地址(可选)"
    )
    
    # 响应时间相关字段
    last_response_time: float = Column(
        Float,
        nullable=True,
        comment="最近一次响应时间(毫秒)"
    )
    avg_response_time: float = Column(
        Float,
        nullable=True,
        comment="平均响应时间(毫秒)"
    )
    min_response_time: float = Column(
        Float,
        nullable=True,
        comment="最小响应时间(毫秒)"
    )
    max_response_time: float = Column(
        Float,
        nullable=True,
        comment="最大响应时间(毫秒)"
    )
    test_count: int = Column(
        Integer,
        default=0,
        comment="测试次数"
    )
    last_test_time: DateTime = Column(
        DateTime,
        nullable=True,
        comment="最近测试时间"
    )

    # 关联用户
    user = relationship("User", back_populates="llm_channels")

    def __repr__(self) -> str:
        return f"<LLMChannel {self.channel_name} ({self.model_type}/{self.model})>"

    def update_response_time(self, response_time: float) -> None:
        """
        更新响应时间统计
        Args:
            response_time: 新的响应时间(毫秒)
        """
        self.last_response_time = response_time
        self.last_test_time = datetime.now()
        self.test_count += 1
        
        # 更新最大最小值
        if self.min_response_time is None or response_time < self.min_response_time:
            self.min_response_time = response_time
        if self.max_response_time is None or response_time > self.max_response_time:
            self.max_response_time = response_time
            
        # 更新平均值
        if self.avg_response_time is None:
            self.avg_response_time = response_time
        else:
            # 使用增量平均值计算
            self.avg_response_time = (
                (self.avg_response_time * (self.test_count - 1) + response_time)
                / self.test_count
            )