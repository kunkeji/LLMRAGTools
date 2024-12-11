# LLM渠道管理 API 文档

## 接口概述

LLM渠道管理API用于管理用户的LLM（大语言模型）渠道配置，包括创建、查询、更新和删除渠道等操作。

## 基础信息

- **基础路径**: `/api/v1/user/channels`
- **认证方式**: Bearer Token
- **请求格式**: JSON
- **响应格式**: JSON

## 通用响应格式

```json
{
    "code": "200",        // 状态码
    "message": "Success", // 响应消息
    "data": {            // 响应数据
        // 具体数据字段
    }
}
```

## 接口列表

### 1. 创建渠道

创建新的LLM渠道配置。

- **请求方法**: `POST`
- **请求路径**: `/api/v1/user/channels`
- **请求头**:
  ```
  Authorization: Bearer {token}
  Content-Type: application/json
  ```

- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| channel_name | string | 是 | 渠道名称 | "我的智谱渠道" |
| model_type | string | 是 | 模型类型 | "zhipu" |
| model | string | 是 | 具体模型 | "glm-4" |
| api_key | string | 是 | API密钥 | "your-api-key" |
| proxy_url | string | 否 | 代理地址 | "http://proxy.example.com" |

- **请求示例**:
```json
{
    "channel_name": "我的智谱渠道",
    "model_type": "zhipu",
    "model": "glm-4",
    "api_key": "your-api-key-here",
    "proxy_url": "http://proxy.example.com"
}
```

- **响应示例**:
```json
{
    "code": "200",
    "message": "Success",
    "data": {
        "id": 1,
        "user_id": 123,
        "channel_name": "我的智谱渠道",
        "model_type": "zhipu",
        "model": "glm-4",
        "api_key": "your-api-key-here",
        "proxy_url": "http://proxy.example.com"
    }
}
```

### 2. 获取渠道列表

获取当前用户的所有LLM渠道。

- **请求方法**: `GET`
- **请求路径**: `/api/v1/user/channels`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

- **查询参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| skip | integer | 否 | 跳过记录数 | 0 |
| limit | integer | 否 | 返回记录数 | 10 |
| keyword | string | 否 | 搜索关键词 | "智谱" |
| model_type | string | 否 | 模型类型筛选 | "zhipu" |

- **响应示例**:
```json
{
    "code": "200",
    "message": "Success",
    "data": [
        {
            "id": 1,
            "user_id": 123,
            "channel_name": "我的智谱渠道",
            "model_type": "zhipu",
            "model": "glm-4",
            "api_key": "your-api-key-here",
            "proxy_url": "http://proxy.example.com"
        }
    ]
}
```

### 3. 获取渠道详情

获取指定渠道的详细信息。

- **请求方法**: `GET`
- **请求路径**: `/api/v1/user/channels/{channel_id}`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| channel_id | integer | 是 | 渠道ID | 1 |

- **响应示例**:
```json
{
    "code": "200",
    "message": "Success",
    "data": {
        "id": 1,
        "user_id": 123,
        "channel_name": "我的智谱渠道",
        "model_type": "zhipu",
        "model": "glm-4",
        "api_key": "your-api-key-here",
        "proxy_url": "http://proxy.example.com"
    }
}
```

### 4. 更新渠道

更新指定渠道的配置信息。

- **请求方法**: `PUT`
- **请求路径**: `/api/v1/user/channels/{channel_id}`
- **请求头**:
  ```
  Authorization: Bearer {token}
  Content-Type: application/json
  ```

- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| channel_id | integer | 是 | 渠道ID | 1 |

- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| channel_name | string | 否 | 渠道名称 | "新的渠道名称" |
| model_type | string | 否 | 模型类型 | "zhipu" |
| model | string | 否 | 具体模型 | "glm-4" |
| api_key | string | 否 | API密钥 | "new-api-key" |
| proxy_url | string | 否 | 代理地址 | "new-proxy-url" |

- **请求示例**:
```json
{
    "channel_name": "新的渠道名称",
    "api_key": "new-api-key"
}
```

- **响应示例**:
```json
{
    "code": "200",
    "message": "Success",
    "data": {
        "id": 1,
        "user_id": 123,
        "channel_name": "新的渠道名称",
        "model_type": "zhipu",
        "model": "glm-4",
        "api_key": "new-api-key",
        "proxy_url": "http://proxy.example.com"
    }
}
```

### 5. 删除渠道

删除指定的渠道配置。

- **请求方法**: `DELETE`
- **请求路径**: `/api/v1/user/channels/{channel_id}`
- **请求头**:
  ```
  Authorization: Bearer {token}
  ```

- **路径参数**:

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| channel_id | integer | 是 | 渠道ID | 1 |

- **响应示例**:
```json
{
    "code": "200",
    "message": "删除成功",
    "data": null
}
```

## 错误码说明

| 错误码 | 说明 | 示例场景 |
|--------|------|----------|
| 400 | 请求参数错误 | 渠道名称已存在 |
| 401 | 未认证或认证失败 | Token无效或已过期 |
| 403 | 无权限访问 | 尝试访问其他用户的渠道 |
| 404 | 渠道不存在 | 访问已删除的渠道 |
| 500 | 服务器内部错误 | 服务器异常 |

## 注意事项

1. **安全性**
   - API密钥等敏感信息在传输和存储时都会进行加密处理
   - 所有接口都需要用户登录认证
   - 用户只能访问和管理自己创建的渠道

2. **限制说明**
   - 渠道名称在同一用户下必须唯一
   - 字段长度限制：
     - channel_name: 最大100字符
     - model_type: 最大50字符
     - model: 最大50字符
     - api_key: 最大500字符
     - proxy_url: 最大200字符

3. **最佳实践**
   - 建议定期更新API密钥以提高安全性
   - 使用有意义的渠道名称便于管理
   - 在更新渠道信息时，仅传递需要更新的字段
   