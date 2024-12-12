"""
LLM渠道管理的Schema
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class LLMChannelBase(BaseModel):
    """LLM渠道基础Schema"""
    channel_name: str = Field(..., description="渠道名称", max_length=100)
    model_type: str = Field(..., description="模型类型", max_length=50)
    model: str = Field(..., description="具体模型", max_length=50)
    api_key: str = Field(..., description="API密钥", max_length=500)
    proxy_url: Optional[str] = Field(None, description="代理地址(可选)", max_length=200)

class LLMChannelCreate(LLMChannelBase):
    """创建LLM渠道时的Schema"""
    pass

class LLMChannelUpdate(BaseModel):
    """更新LLM渠道时的Schema"""
    channel_name: Optional[str] = Field(None, description="渠道名称", max_length=100)
    model_type: Optional[str] = Field(None, description="模型类型", max_length=50)
    model: Optional[str] = Field(None, description="具体模型", max_length=50)
    api_key: Optional[str] = Field(None, description="API密钥", max_length=500)
    proxy_url: Optional[str] = Field(None, description="代理地址", max_length=200)

class LLMChannelPerformance(BaseModel):
    """渠道性能统计Schema"""
    last_response_time: Optional[float] = Field(None, description="最近一次响应时间(毫秒)")
    avg_response_time: Optional[float] = Field(None, description="平均响应时间(毫秒)")
    min_response_time: Optional[float] = Field(None, description="最小响应时间(毫秒)")
    max_response_time: Optional[float] = Field(None, description="最大响应时间(毫秒)")
    test_count: int = Field(0, description="测试次数")
    last_test_time: Optional[datetime] = Field(None, description="最近测试时间")

class LLMChannel(LLMChannelBase):
    """返回给前端的LLM渠道Schema"""
    id: int
    user_id: int
    last_response_time: Optional[float] = None
    avg_response_time: Optional[float] = None
    min_response_time: Optional[float] = None
    max_response_time: Optional[float] = None
    test_count: int = 0
    last_test_time: Optional[datetime] = None

    class Config:
        from_attributes = True 