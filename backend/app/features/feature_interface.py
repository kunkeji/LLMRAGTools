"""
LLM功能映射接口工具类
"""
from typing import AsyncGenerator
from sqlalchemy.orm import Session
from app.models.llm_feature import FeatureType
from app.crud.llm_feature_mapping import crud_feature_mapping
from app.utils.llm.client import LLMClient
from app.core.exceptions import FeatureNotConfiguredError

class FeatureInterface:
    """功能映射接口工具类"""
    
    @staticmethod
    async def execute_feature_stream(
        db: Session,
        user_id: int,
        feature_type: FeatureType,
        message: str
    ) -> AsyncGenerator[str, None]:
        """执行特定功能并返回流式响应
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            feature_type: 功能类型
            message: 用户输入的消息
            
        Yields:
            str: 流式响应内容
            
        Raises:
            FeatureNotConfiguredError: 功能未配置错误
        """
        try:
            # 获取用户的功能映射配置
            mapping = crud_feature_mapping.get_by_feature_type(
                db=db,
                user_id=user_id,
                feature_type=feature_type
            )
            
            if not mapping:
                raise FeatureNotConfiguredError(f"功能 {feature_type} 未配置")
                
            # 获取提示词模板
            prompt_template = mapping.prompt_template or mapping.feature.default_prompt
            
            # 使用LLM客户端生成流式响应
            async for chunk in LLMClient.generate_stream(
                prompt=prompt_template,
                message=message,
                api_key=mapping.channel.api_key,
                provider=mapping.channel.model_type,
                model=mapping.channel.model,
                proxy_url=mapping.channel.proxy_url
            ):
                yield chunk  # 添加换行符以确保正确的流式输出
            # 更新使用统计
            mapping.update_usage()
            db.add(mapping)
            db.commit()  # 同步提交数据库事务
            
        except Exception as e:
            # 确保异常也能正确地流式输出
            yield f"Error: {str(e)}\n"
            raise