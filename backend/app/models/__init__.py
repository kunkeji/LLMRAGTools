"""
数据库模型初始化
"""
from app.models.base_model import BaseDBModel
from app.models.user import User
from app.models.admin import Admin
from app.models.verification_code import VerificationCode
from app.models.llm_model import LLMModel
from app.models.llm_channel import LLMChannel
from app.models.email_provider import EmailProvider
from app.models.email_account import EmailAccount
from app.models.task import Task
from app.models.llm_feature import LLMFeature
from app.models.llm_feature_mapping import LLMFeatureMapping

# 导出所有模型
__all__ = [
    "BaseDBModel",
    "User",
    "Admin",
    "VerificationCode",
    "LLMModel",
    "LLMChannel",
    "EmailProvider",
    "EmailAccount",
    "Task",
    "LLMFeature",
    "LLMFeatureMapping"
]
