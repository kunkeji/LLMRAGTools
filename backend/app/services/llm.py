from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import openai
import anthropic
from app.core.config import settings
from app.crud.llm import get_model, get_channel, get_feature, get_feature_mapping

# 线程池配置
executor = ThreadPoolExecutor(max_workers=settings.LLM_MAX_WORKERS)

class LLMService:
    def __init__(self):
        self.models = {}
        self.channels = {}
        self.features = {}
        self.mappings = {}

    async def init_channel(self, channel_id: int) -> Dict[str, Any]:
        """初始化渠道配置"""
        if channel_id in self.channels:
            return self.channels[channel_id]

        channel = await get_channel(channel_id)
        if not channel:
            raise ValueError(f"Channel {channel_id} not found")

        model = await get_model(channel.model_id)
        if not model:
            raise ValueError(f"Model {channel.model_id} not found")

        config = {
            "channel": channel,
            "model": model,
            "client": self._create_client(model)
        }
        self.channels[channel_id] = config
        return config

    def _create_client(self, model: Dict[str, Any]) -> Any:
        """创建LLM客户端"""
        if model["type"] == "openai":
            openai.api_key = model["config"]["api_key"]
            return openai
        elif model["type"] == "anthropic":
            return anthropic.Anthropic(api_key=model["config"]["api_key"])
        else:
            raise ValueError(f"Unsupported model type: {model['type']}")

    async def get_feature_config(self, channel_id: int, feature_id: int) -> Dict[str, Any]:
        """获取特性配置"""
        key = f"{channel_id}_{feature_id}"
        if key in self.mappings:
            return self.mappings[key]

        feature = await get_feature(feature_id)
        if not feature:
            raise ValueError(f"Feature {feature_id} not found")

        mapping = await get_feature_mapping(channel_id, feature_id)
        if not mapping:
            raise ValueError(f"Feature mapping not found for channel {channel_id} and feature {feature_id}")

        config = {
            "feature": feature,
            "mapping": mapping
        }
        self.mappings[key] = config
        return config

    async def process_request(self, channel_id: int, feature_id: int, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理LLM请求"""
        channel_config = await self.init_channel(channel_id)
        feature_config = await self.get_feature_config(channel_id, feature_id)

        # 根据模型类型处理请求
        if channel_config["model"]["type"] == "openai":
            return await self._process_openai_request(channel_config, feature_config, params)
        elif channel_config["model"]["type"] == "anthropic":
            return await self._process_anthropic_request(channel_config, feature_config, params)
        else:
            raise ValueError(f"Unsupported model type: {channel_config['model']['type']}")

    async def _process_openai_request(
        self, 
        channel_config: Dict[str, Any], 
        feature_config: Dict[str, Any], 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """处理OpenAI请求"""
        model = channel_config["model"]["config"]["model"]
        prompt = self._format_prompt(feature_config["mapping"]["config"]["prompt_template"], params)
        
        try:
            response = await channel_config["client"].ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=feature_config["feature"]["config"].get("temperature", 0.7),
                max_tokens=feature_config["feature"]["config"].get("max_tokens", 2000)
            )
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "usage": response.usage
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    async def _process_anthropic_request(
        self, 
        channel_config: Dict[str, Any], 
        feature_config: Dict[str, Any], 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """处理Anthropic请求"""
        model = channel_config["model"]["config"]["model"]
        prompt = self._format_prompt(feature_config["mapping"]["config"]["prompt_template"], params)
        
        try:
            response = await channel_config["client"].messages.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=feature_config["feature"]["config"].get("temperature", 0.7),
                max_tokens=feature_config["feature"]["config"].get("max_tokens", 4000)
            )
            return {
                "success": True,
                "content": response.content[0].text,
                "usage": response.usage
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _format_prompt(self, template: str, params: Dict[str, Any]) -> str:
        """格式化提示词"""
        return template.format(**params)

    async def process_request_in_thread(
        self, 
        channel_id: int, 
        feature_id: int, 
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """在线程池中处理请求"""
        future = executor.submit(self.process_request, channel_id, feature_id, params)
        return await future.result()

# 全局LLM服务实例
llm_service = LLMService() 