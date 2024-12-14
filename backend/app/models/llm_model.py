"""
大语言模型信息模型
"""
from sqlalchemy import Column, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.models.base_model import BaseDBModel

class ModelStatus(str, Enum):
    """模型状态"""
    ACTIVE = "ACTIVE"        # 正常使用
    INACTIVE = "INACTIVE"    # 已停用

class LLMModel(BaseDBModel):
    """大语言模型信息"""
    __tablename__ = "llm_models"

    name: str = Column(
        String(100), 
        nullable=False, 
        unique=True,
        index=True,
        comment="模型名称(如智谱AI、通义千问等)"
    )
    mapping_name: str = Column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="映射名称(如zhipu、qwen等)"
    )
    status: ModelStatus = Column(
        SQLEnum(ModelStatus, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        default=ModelStatus.ACTIVE,
        comment="模型状态"
    )
    is_public: bool = Column(
        Boolean,
        default=True,
        comment="是否公开可用"
    )
    description: str = Column(
        String(500),
        nullable=True,
        comment="模型描述"
    )
    
    def __repr__(self) -> str:
        return f"<LLMModel {self.name} ({self.mapping_name})>" 