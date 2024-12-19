from typing import Any, AsyncGenerator
import requests
import json
import re

from sqlalchemy import true

def generate(prompt: str, message: str, api_key: str, model: str, proxy_url: str, **kwargs: Any) -> str:
    # 请求RAGflow API proxy_url
    headers = {
        'content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "question":prompt + message,
        "stream": False,
        "session_id":'74531518bdde11efa70400155dadeedc'
    }
    agent_id = model
    response = requests.post(f'{proxy_url}/api/v1/agents/{agent_id}/completions', headers=headers, data=json.dumps(data))
    print(response.json())
    response.raise_for_status()
    return response.json()['answer']
    # 返回文本

async def generate_stream(prompt: str, message: str, api_key: str, model: str, proxy_url: str, **kwargs: Any) -> AsyncGenerator[str, None]:
    # 请求RAGflow API proxy_url
    headers = {
        'content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "question": prompt + message,
        "stream": True,
        "session_id": '74531518bdde11efa70400155dadeedc'
    }

    agent_id = model
    response = requests.post(f'{proxy_url}/api/v1/agents/{agent_id}/completions', headers=headers, data=json.dumps(data), stream=True)
    
    previous_length = 0  # 记录上一次答案的长度
    for chunk in response.iter_content(chunk_size=None):  # 使用 None 作为 chunk_size，让请求自动处理分块
        if chunk:
            try:
                # 将字节转换为字符串
                chunk_str = chunk.decode('utf-8')
                if chunk_str.startswith('data:'):
                    # 移除 'data:' 前缀并解析 JSON
                    json_str = chunk_str[5:].strip()
                    chunk_data = json.loads(json_str)
                    
                    if 'data' in chunk_data:
                        if isinstance(chunk_data['data'], dict) and 'answer' in chunk_data['data']:
                            answer = chunk_data['data']['answer']
                            if isinstance(answer, str):
                                # 检查是否是运行提示信息
                                if re.match(r'\*.*?\* is running...🕞', answer):
                                    # print("跳过运行提示信息")  # 调试信息
                                    continue
                                # 获取新增的内容
                                new_content = answer[previous_length:]
                                # print(f"新增内容: {new_content}")  # 调试信息
                                if new_content:
                                    yield new_content
                                previous_length = len(answer)
                        elif chunk_data['data'] is True:
                            break
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"解析错误: {e}")  # 调试信息
                continue


