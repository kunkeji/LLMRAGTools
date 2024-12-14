"""
智谱AI SDK调用实现
"""
from typing import Optional, Dict, Any, AsyncGenerator
from zhipuai import ZhipuAI

def generate(
    prompt: str,
    message: str,
    api_key: str,
    model: str = "glm-4-flash",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs: Any
) -> str:
    """
    生成文本
    
    Args:
        prompt: 提示文本
        api_key: 智谱API密钥
        model: 模型名称
        temperature: 温度
        max_tokens: 最大生成token数
        message: 消息列表
        **kwargs: 其他参数
    """
    client = ZhipuAI(api_key=api_key)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )
    
    return response.choices[0].message.content

async def generate_stream(
    prompt: str,
    message: str,
    api_key: str,
    model: str = "glm-4-flash",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    **kwargs: Any
) -> AsyncGenerator[str, None]:
    """
    流式生成文本
    
    Args:
        prompt: 提示文本
        api_key: 智谱API密钥
        model: 模型名称
        temperature: 温度
        max_tokens: 最大生成token数
        **kwargs: 其他参数
    """
    client = ZhipuAI(api_key=api_key)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message}
    ]
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=True,
        **kwargs
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
