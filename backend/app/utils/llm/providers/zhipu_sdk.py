from typing import Optional, Dict, Any, AsyncGenerator
from zhipuai import ZhipuAI

def generate(
    prompt: str,
    message: str,
    api_key: str,
    model: str = "glm-4-flash",
    temperature: float = 0.7,
    max_tokens: Optional[int] = None,
    proxy_url: Optional[str] = None,
    **kwargs: Any
) -> str:
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
    proxy_url: Optional[str] = None,
    **kwargs: Any
) -> AsyncGenerator[str, None]:
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
