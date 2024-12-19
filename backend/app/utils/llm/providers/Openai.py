import os
from typing import Any, AsyncGenerator
from openai import OpenAI



def generate(prompt: str, message: str, api_key: str, model: str, proxy_url: str, **kwargs: Any) -> str:
    os.environ['OPENAI_API_KEY'] = api_key
    client = OpenAI(
        base_url=proxy_url,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": message}],
        **kwargs
    )
    return response.choices[0].message.content

async def generate_stream(prompt: str, message: str, api_key: str, model: str, proxy_url: str, **kwargs: Any) -> AsyncGenerator[str, None]:
    os.environ['OPENAI_API_KEY'] = api_key
    client = OpenAI(
        base_url=proxy_url,
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}, {"role": "user", "content": message}],
        stream=True,
        **kwargs
    )
    for chunk in response:
        try:
            if chunk.choices and len(chunk.choices) > 0:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"处理chunk时出错: {e}")
            continue

