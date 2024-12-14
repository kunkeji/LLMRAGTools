# LLM功能映射接口文档

## 获取LLM模型列表

获取系统中所有可用的LLM模型。

### 请求

```http
GET /api/v1/user/llm/models
```

### 响应

```json
{
    "code": 0,
    "message": "success",
    "data": [
        {
            "id": 1,
            "name": "GPT-3.5",
            "provider": "openai",
            "model_type": "gpt-3.5-turbo",
            "description": "OpenAI GPT-3.5 Turbo模型",
            "is_active": true,
            "created_at": "2023-12-13T10:00:00",
            "updated_at": "2023-12-13T10:00:00"
        }
    ]
}
```

## 获取功能列表

获取系统支持的所有LLM功能。

### 请求

```http
GET /api/v1/user/feature-mappings/features
```

### 响应

```json
{
    "code": 0,
    "message": "success",
    "data": [
        {
            "feature_type": "document_write",
            "name": "文档写作",
            "description": "AI辅助文档写作",
            "default_prompt": "你是一个专业的文档写作助手..."
        }
    ]
}
```

## 获取用户映射配置

获取用户的功能映射配置。

### 请求

```http
GET /api/v1/user/feature-mappings/mappings
```

### 响应

```json
{
    "code": 0,
    "message": "success",
    "data": [
        {
            "id": 1,
            "user_id": 123,
            "channel_id": 1,
            "feature_type": "document_write",
            "prompt_template": "自定义的提示词模板...",
            "last_used_at": "2023-12-13T10:00:00",
            "use_count": 10
        }
    ]
}
```

## 保存功能映射

保存用户的功能映射配置(新增或更新)。

### 请求

```http
POST /api/v1/user/feature-mappings/mappings/save
```

### 请求参数

```json
{
    "channel_id": 1,
    "feature_type": "document_write",
    "prompt_template": "自定义的提示词模板..."  // 可选
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| channel_id | integer | 是 | 渠道ID |
| feature_type | string | 是 | 功能类型(document_write/document_improve/document_summary等) |
| prompt_template | string | 否 | 自定义提示词模板,不填则使用默认模板 |

### 响应

```json
{
    "code": 0,
    "message": "success",
    "data": {
        "id": 1,
        "user_id": 123,
        "channel_id": 1,
        "feature_type": "document_write",
        "prompt_template": "自定义的提示词模板...",
        "last_used_at": null,
        "use_count": 0,
        "created_at": "2023-12-13T10:00:00",
        "updated_at": "2023-12-13T10:00:00"
    }
}
```

## 功能类型说明

| 功能类型 | 说明 |
|----------|------|
| document_write | 文档写作 |
| document_improve | 文档改进 |
| document_summary | 文档总结 |
| document_translate | 文档翻译 |
| code_comment | 代码注释 |
| code_review | 代码审查 |
| code_optimize | 代码优化 |