"""
LLM统一调用工具
"""
from typing import Optional, Dict, Any, AsyncGenerator
from .providers import zhipu_sdk
from .mapping import DEFAULT_PROVIDER, MODEL_MAPPING

class LLMClient:
    """LLM调用客户端"""
    
    _providers = {
        "zhipu": zhipu_sdk
    }
    
    @staticmethod
    def generate(
        prompt: str,
        message: str,
        api_key: str,
        provider: str = DEFAULT_PROVIDER,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> str:
        """
        生成文本
        
        Args:
            prompt: 提示文本
            api_key: API密钥
            provider: LLM提供者名称
            model: 模型名称
            **kwargs: 其他参数
        """
        # 获取提供者模块
        if provider not in LLMClient._providers:
            raise ValueError(f"不支持的LLM提供者: {provider}")
            
        sdk = LLMClient._providers[provider]
        
        # 处理模型名称
        if model and model in MODEL_MAPPING:
            model = MODEL_MAPPING[model]
            
        # 调用对应的SDK
        return sdk.generate(prompt, message, api_key=api_key, model=model, **kwargs)
    
    @staticmethod
    async def generate_stream(
        prompt: str,
        message: str,
        api_key: str,
        provider: str = DEFAULT_PROVIDER,
        model: Optional[str] = None,
        **kwargs: Any
    ) -> AsyncGenerator[str, None]:
        """
        流式生成文本
        
        Args:
            prompt: 提示文本
            api_key: API密钥
            provider: LLM提供者名称
            model: 模型名称
            **kwargs: 其他参数
            
        Yields:
            str: 生成的文本片段
        """
        # 获取提供者模块
        if provider not in LLMClient._providers:
            raise ValueError(f"不支持的LLM提供者: {provider}")
            
        sdk = LLMClient._providers[provider]
        
        # 处理模型名称
        if model and model in MODEL_MAPPING:
            model = MODEL_MAPPING[model]
        
        # 调用对应的SDK
        async for chunk in sdk.generate_stream(prompt, message, api_key=api_key, model=model, **kwargs):
            yield chunk