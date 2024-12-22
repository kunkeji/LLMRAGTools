# API 文档

## 基础信息

- 基础URL: `http://localhost:8111` (开发环境)
- API版本: v1
- 认证方式: Bearer Token

## 认证

### 获取Token
```http
POST /api/v1/user/login
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

响应:
```json
{
    "code": 200,
    "data": {
        "access_token": "string",
        "token_type": "bearer"
    },
    "message": "success"
}
```

## 用户相关接口

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

### 获取用户信息
```http
GET /api/v1/user/me
Authorization: Bearer {token}
```

### 更新用户信息
```http
PUT /api/v1/user/me
Authorization: Bearer {token}
Content-Type: application/json

{
    "nickname": "string",
    "avatar": "string",
    "email": "user@example.com"
}
```

## 邮件系统接口

### 邮箱账户管理

#### 添加邮箱账户
```http
POST /api/v1/user/email-accounts
Authorization: Bearer {token}
Content-Type: application/json

{
    "email": "string",
    "password": "string",
    "provider_id": "integer",
    "name": "string"
}
```

#### 获取邮箱账户列表
```http
GET /api/v1/user/email-accounts
Authorization: Bearer {token}
```

#### 更新邮箱账户
```http
PUT /api/v1/user/email-accounts/{account_id}
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "password": "string"
}
```

### 邮件管理

#### 获取邮件列表
```http
GET /api/v1/user/emails
Authorization: Bearer {token}
Query Parameters:
- page: integer (默认: 1)
- per_page: integer (默认: 20)
- folder: string
- tag_id: integer
- search: string
```

#### 发送邮件
```http
POST /api/v1/user/emails
Authorization: Bearer {token}
Content-Type: application/json

{
    "account_id": "integer",
    "to": ["string"],
    "cc": ["string"],
    "bcc": ["string"],
    "subject": "string",
    "content": "string",
    "attachments": ["string"]
}
```

### 邮件标签

#### 创建标签
```http
POST /api/v1/user/email-tags
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "color": "string"
}
```

#### 获取标签列表
```http
GET /api/v1/user/email-tags
Authorization: Bearer {token}
```

## LLM功能接口

### 模型管理

#### 获取模型列表
```http
GET /api/v1/admin/llm-models
Authorization: Bearer {token}
```

#### 添加模型
```http
POST /api/v1/admin/llm-models
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "type": "string",
    "config": {}
}
```

### 渠道管理

#### 获取渠道列表
```http
GET /api/v1/admin/llm-channels
Authorization: Bearer {token}
Query Parameters:
- page: integer (默认: 1)
- per_page: integer (固定: 10)
```

#### 添加渠道
```http
POST /api/v1/admin/llm-channels
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "config": {},
    "model_id": "integer"
}
```

#### 测试渠道
```http
POST /api/v1/admin/llm-channels/{channel_id}/test
Authorization: Bearer {token}
Content-Type: application/json

{
    "prompt": "string"
}
```

### 特性管理

#### 获取特性列表
```http
GET /api/v1/admin/llm-features
Authorization: Bearer {token}
```

#### 添加特性
```http
POST /api/v1/admin/llm-features
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "type": "string",
    "config": {}
}
```

## 文档管理接口

### 获取文档列表
```http
GET /api/v1/user/documents
Authorization: Bearer {token}
Query Parameters:
- page: integer (默认: 1)
- per_page: integer (默认: 20)
- type: string
```

### 上传文档
```http
POST /api/v1/user/documents
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: (binary)
type: string
description: string
```

## 系统管理接口

### 日志管理

#### 获取操作日志
```http
GET /api/v1/admin/logs
Authorization: Bearer {token}
Query Parameters:
- page: integer (默认: 1)
- per_page: integer (默认: 20)
- type: string
- start_time: string
- end_time: string
```

### 任务管理

#### 获取任务列表
```http
GET /api/v1/admin/tasks
Authorization: Bearer {token}
Query Parameters:
- page: integer (默认: 1)
- per_page: integer (默认: 20)
- status: string
```

#### 创建定时任务
```http
POST /api/v1/admin/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "string",
    "type": "string",
    "schedule": "string",
    "config": {}
}
```

## 错误码说明

- 200: 成功
- 400: 请求参数错误
- 401: 未认证
- 403: 无权限
- 404: 资源不存在
- 500: 服务器内部错误

## 通用响应格式

成功响应:
```json
{
    "code": 200,
    "data": {},
    "message": "success"
}
```

错误响应:
```json
{
    "code": 400,
    "message": "error message",
    "data": null
}
``` 