# LLM 映射功能文档

## 概述

LLM 映射功能是 LLMRAGTools 框架的核心特性之一，它提供了一个灵活的机制来管理和使用不同的大语言模型（LLM）。通过映射功能，开发者可以：

1. 统一调用接口
2. 灵活切换模型
3. 管理模型参数
4. 控制调用成本

## 映射配置

### 基础配置结构

```python
{
    "model_name": {
        "provider": "provider_name",
        "model": "actual_model_name",
        "temperature": float,
        "max_tokens": int,
        "additional_params": {}
    }
}
```

### 示例配置

```python
{
    "gpt-4": {
        "provider": "openai",
        "model": "gpt-4-1106-preview",
        "temperature": 0.7,
        "max_tokens": 2000
    },
    "claude": {
        "provider": "anthropic",
        "model": "claude-2.1",
        "temperature": 0.9,
        "max_tokens": 4000
    },
    "chatglm": {
        "provider": "zhipu",
        "model": "chatglm_turbo",
        "temperature": 0.8,
        "max_tokens": 2000
    }
}
```

## 使用方法

### 1. 基础调用

```python
from app.utils.llm import LLMClient

# 普通对话
response = await LLMClient.generate(
    prompt="你是一个专业的助手",
    message="帮我总结这篇文章",
    model="gpt-4"  # 将自动映射到配置的模型
)

# 流式对话
async for chunk in LLMClient.generate_stream(
    prompt="你是一个专业的助手",
    message="帮我总结这篇文章",
    model="claude"
):
    print(chunk, end="")
```

### 2. 自定义参数

```python
response = await LLMClient.generate(
    prompt="你是一个专业的助手",
    message="帮我总结这篇文章",
    model="gpt-4",
    temperature=0.5,  # 覆盖默认温度
    max_tokens=1000   # 覆盖默认最大token数
)
```

### 3. 批量处理

```python
async def process_batch(messages):
    tasks = []
    for msg in messages:
        task = LLMClient.generate(
            prompt="你是一个专业的助手",
            message=msg,
            model="gpt-4"
        )
        tasks.append(task)
    return await asyncio.gather(*tasks)
```

## 添加新的提供商

### 1. 创建提供商类

```python
from app.utils.llm.base import BaseLLMProvider

class NewProvider(BaseLLMProvider):
    def __init__(self, config):
        super().__init__(config)
        # 初始化提供商特定的配置
        
    async def generate(self, prompt, message, **kwargs):
        # 实现生成方法
        pass
        
    async def generate_stream(self, prompt, message, **kwargs):
        # 实现流式生成方法
        pass
```

### 2. 注册提供商

```python
from app.utils.llm.registry import provider_registry

provider_registry.register("new_provider", NewProvider)
```

### 3. 添加映射配置

```python
{
    "custom-model": {
        "provider": "new_provider",
        "model": "model_name",
        "temperature": 0.7
    }
}
```

## 错误处理

### 1. 重试机制

```python
from app.utils.llm.retry import retry_with_exponential_backoff

@retry_with_exponential_backoff(max_retries=3)
async def generate_with_retry():
    return await LLMClient.generate(...)
```

### 2. 错误类型

```python
from app.utils.llm.exceptions import (
    LLMProviderError,
    LLMAuthenticationError,
    LLMRateLimitError,
    LLMInvalidRequestError
)

try:
    response = await LLMClient.generate(...)
except LLMRateLimitError:
    # 处理速率限制错误
    pass
except LLMAuthenticationError:
    # 处理认证错误
    pass
```

## 成本控制

### 1. Token 计数

```python
from app.utils.llm.token_counter import count_tokens

tokens = count_tokens("要计数的文本", model="gpt-4")
```

### 2. 成本估算

```python
from app.utils.llm.cost import estimate_cost

cost = estimate_cost(
    input_tokens=100,
    output_tokens=50,
    model="gpt-4"
)
```

## 最佳实践

1. **模型选择**
   - 根据任务复杂度选择合适的模型
   - 考虑成本和性能的平衡

2. **参数调优**
   - 根据场景调整温度参数
   - 合理设置最大token数
   - 适当使用重试机制

3. **错误处理**
   - 实现完善的错误处理逻辑
   - 使用重试机制处理临时错误
   - 记录详细的错误日志

4. **成本优化**
   - 合理使用token计数
   - 实现成本控制策略
   - 监控API调用情况

## 监控和日志

### 1. 调用日志

```python
from app.utils.llm.logging import log_llm_call

await log_llm_call(
    model="gpt-4",
    input_tokens=100,
    output_tokens=50,
    cost=0.002,
    duration=1.5
)
```

### 2. 性能监控

```python
from app.utils.llm.metrics import track_performance

await track_performance(
    model="gpt-4",
    latency=1.5,
    success=True
)
```

## 配置示例

### 1. 环境变量

```bash
OPENAI_API_KEY=sk-xxx
ANTHROPIC_API_KEY=sk-xxx
ZHIPU_API_KEY=xxx
```

### 2. 模型配置

```python
LLM_CONFIG = {
    "default_model": "gpt-4",
    "timeout": 30,
    "max_retries": 3,
    "models": {
        "gpt-4": {
            "provider": "openai",
            "model": "gpt-4-1106-preview",
            "temperature": 0.7
        },
        "claude": {
            "provider": "anthropic",
            "model": "claude-2.1",
            "temperature": 0.9
        }
    }
}
``` 