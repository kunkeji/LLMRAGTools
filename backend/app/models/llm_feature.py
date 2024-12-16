"""
LLM功能定义模型
"""
from sqlalchemy import Column, String, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum
from app.models.base_model import BaseDBModel

class FeatureType(str, Enum):
    """功能类型枚举"""
    DOCUMENT_WRITE = "DOCUMENT_WRITE"      # 文档写作
    DOCUMENT_IMPROVE = "DOCUMENT_IMPROVE"  # 文档改进
    DOCUMENT_SUMMARY = "DOCUMENT_SUMMARY"  # 文档总结
    DOCUMENT_TRANSLATE = "DOCUMENT_TRANSLATE"  # 文档翻译
    LABEL_CLASSIFICATION = "LABEL_CLASSIFICATION"  # 标签分类
    EMAIL_REPLY = "EMAIL_REPLY"  # 邮件回复

class LLMFeature(BaseDBModel):
    """LLM功能定义"""
    __tablename__ = "llm_features"

    feature_type: str = Column(
        SQLEnum(FeatureType),
        primary_key=True,
        index=True,
        comment="功能类型"
    )
    
    name: str = Column(
        String(100),
        nullable=False,
        comment="功能名称"
    )
    
    description: str = Column(
        Text,
        nullable=True,
        comment="功能描述"
    )
    
    default_prompt: str = Column(
        Text,
        nullable=False,
        comment="默认提示词模板"
    )
    
    # 关联关系
    feature_mappings = relationship(
        "LLMFeatureMapping",
        back_populates="feature",
        lazy="select",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str:
        return f"<LLMFeature {self.name} ({self.feature_type})>" 