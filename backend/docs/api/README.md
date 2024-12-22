# API 接口文档

## 基础信息

- 基础URL: `http://localhost:8111`
- API版本: v1
- 认证方式: Bearer Token
- 响应格式: JSON

## 通用规范

### 请求头
```http
Content-Type: application/json
Authorization: Bearer {token}
```

### 响应格式
```json
{
    "code": 200,          // 状态码
    "message": "success", // 响应消息
    "data": {            // 响应数据
        // 具体数据
    }
}
```

### 分页参数
支持分页的接口使用以下查询参数：
- `page`: 页码（从1开始）
- `per_page`: 每页记录数
- `sort`: 排序字段
- `order`: 排序方向（asc/desc）

### 错误码
| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证或认证失败 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 认证接口

### 用户注册
```http
POST /api/v1/user/register
Content-Type: application/json

{
    "username": "string",
    "email": "user@example.com",
    "password": "string"
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "username": "string",
        "email": "user@example.com",
        "created_at": "2024-01-20T08:30:00Z"
    }
}
```

### 用户登录
```http
POST /api/v1/user/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "access_token": "string",
        "token_type": "bearer",
        "expires_in": 1800
    }
}
```

## 用户接口

### 获取用户信息
```http
GET /api/v1/user/me
Authorization: Bearer {token}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "username": "string",
        "email": "user@example.com",
        "nickname": "string",
        "avatar": "string",
        "created_at": "2024-01-20T08:30:00Z"
    }
}
```

### 更新用户信息
```http
PUT /api/v1/user/me
Authorization: Bearer {token}
Content-Type: application/json

{
    "nickname": "string",
    "avatar": "string"
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "username": "string",
        "nickname": "string",
        "avatar": "string"
    }
}
```

## 邮件接口

### 获取邮箱账户列表
```http
GET /api/v1/user/email-accounts
Authorization: Bearer {token}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": 1,
                "email": "user@example.com",
                "name": "工作邮箱",
                "provider_id": 1,
                "is_active": true,
                "last_sync_at": "2024-01-20T08:30:00Z"
            }
        ],
        "total": 1
    }
}
```

### 添加邮箱账户
```http
POST /api/v1/user/email-accounts
Authorization: Bearer {token}
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "string",
    "name": "工作邮箱",
    "provider_id": 1
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "email": "user@example.com",
        "name": "工作邮箱",
        "provider_id": 1,
        "is_active": true
    }
}
```

### 获取邮件列表
```http
GET /api/v1/user/emails
Authorization: Bearer {token}
Query Parameters:
- page: 1
- per_page: 20
- folder: "INBOX"
- tag_id: 1
- search: "string"
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": 1,
                "account_id": 1,
                "message_id": "string",
                "from_address": "sender@example.com",
                "to_address": ["recipient@example.com"],
                "subject": "string",
                "received_at": "2024-01-20T08:30:00Z",
                "is_read": false,
                "tags": [
                    {
                        "id": 1,
                        "name": "重要",
                        "color": "#ff0000"
                    }
                ]
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 20,
        "total_pages": 5
    }
}
```

### 发送邮件
```http
POST /api/v1/user/emails
Authorization: Bearer {token}
Content-Type: application/json

{
    "account_id": 1,
    "to": ["recipient@example.com"],
    "cc": ["cc@example.com"],
    "bcc": ["bcc@example.com"],
    "subject": "string",
    "content": "string",
    "attachments": [
        {
            "filename": "string",
            "content": "base64_string"
        }
    ]
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "status": "sent"
    }
}
```

## LLM 接口

### 获取模型列表
```http
GET /api/v1/llm/models
Authorization: Bearer {token}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": 1,
                "name": "gpt-4",
                "provider": "openai",
                "description": "string",
                "is_active": true
            }
        ]
    }
}
```

### 发送对话请求
```http
POST /api/v1/llm/chat
Authorization: Bearer {token}
Content-Type: application/json

{
    "model": "gpt-4",
    "messages": [
        {
            "role": "system",
            "content": "你是一个专业的助手"
        },
        {
            "role": "user",
            "content": "帮我总结这篇文章"
        }
    ],
    "stream": false
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": "chat_id",
        "model": "gpt-4",
        "response": {
            "role": "assistant",
            "content": "string"
        },
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30
        }
    }
}
```

### 流式对话
```http
POST /api/v1/llm/chat/stream
Authorization: Bearer {token}
Content-Type: application/json

{
    "model": "gpt-4",
    "messages": [
        {
            "role": "system",
            "content": "你是一个专业的助手"
        },
        {
            "role": "user",
            "content": "帮我总结这篇文章"
        }
    ]
}
```

响应（Server-Sent Events）：
```
event: message
data: {"delta": "这", "finish_reason": null}

event: message
data: {"delta": "是", "finish_reason": null}

event: message
data: {"delta": "总结", "finish_reason": null}

event: done
data: {"usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}}
```

## 任务接口

### 创建任务
```http
POST /api/v1/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "type": "string",
    "config": {},
    "schedule": "0 0 * * *"
}
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "name": "string",
        "type": "string",
        "status": "pending",
        "created_at": "2024-01-20T08:30:00Z"
    }
}
```

### 获取任务列表
```http
GET /api/v1/tasks
Authorization: Bearer {token}
Query Parameters:
- page: 1
- per_page: 20
- status: "running"
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": 1,
                "name": "string",
                "type": "string",
                "status": "running",
                "progress": 50,
                "created_at": "2024-01-20T08:30:00Z",
                "started_at": "2024-01-20T08:30:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 20
    }
}
```

## 文件接口

### 上传文件
```http
POST /api/v1/files/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: (binary)
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": 1,
        "filename": "string",
        "size": 1024,
        "mime_type": "string",
        "url": "string"
    }
}
```

### 获取文件列表
```http
GET /api/v1/files
Authorization: Bearer {token}
Query Parameters:
- page: 1
- per_page: 20
- type: "image"
```

响应：
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "items": [
            {
                "id": 1,
                "filename": "string",
                "size": 1024,
                "mime_type": "string",
                "url": "string",
                "created_at": "2024-01-20T08:30:00Z"
            }
        ],
        "total": 100,
        "page": 1,
        "per_page": 20
    }
}
```

## WebSocket 接口

### 实时通知
```javascript
const ws = new WebSocket('ws://localhost:8111/ws/notifications');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log(data);
};
```

消息格式：
```json
{
    "type": "notification",
    "data": {
        "id": 1,
        "type": "email",
        "title": "新邮件",
        "content": "您有一封新邮件",
        "created_at": "2024-01-20T08:30:00Z"
    }
}
```

## 错误处理

### 错误响应格式
```json
{
    "code": 400,
    "message": "错误信息",
    "errors": [
        {
            "field": "username",
            "message": "用户名已存在"
        }
    ]
}
```

### 常见错误
1. 认证错误
```json
{
    "code": 401,
    "message": "认证失败",
    "error": "invalid_token"
}
```

2. 参数错误
```json
{
    "code": 400,
    "message": "参数错误",
    "errors": [
        {
            "field": "email",
            "message": "邮箱格式不正确"
        }
    ]
}
```

3. 权限错误
```json
{
    "code": 403,
    "message": "无权限访问",
    "error": "permission_denied"
}
```

## 最佳实践

1. **认证**
   - 所有请求都应包含有效的 token
   - token 过期前主动刷新
   - 敏感操作使用额外验证

2. **错误处理**
   - 捕获所有可能的错误
   - 合理使用错误码
   - 提供有意义的错误信息

3. **性能优化**
   - 使用分页
   - 合理设置缓存
   - 避免大量请求

4. **安全性**
   - 使用 HTTPS
   - 实现速率限制
   - 验证所有输入 