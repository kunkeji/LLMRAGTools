# 邮件发送接口文档

## 创建待发送邮件

创建一个待发送状态的邮件，不会立即发送。

- **接口**: `POST /api/user/email-outbox/send`
- **权限**: 需要用户登录
- **请求参数**:
```json
{
    "recipients": "string",         // 收件人列表,多个邮箱用分号分隔
    "cc": "string",                // [可选]抄送列表,多个邮箱用分号分隔
    "bcc": "string",               // [可选]密送列表,多个邮箱用分号分隔
    "subject": "string",           // [可选]邮件主题
    "content": "string",           // 邮件内容
    "content_type": "string",      // [可选]内容类型,默认text/html
    "attachments": "string",       // [可选]附件信息,JSON格式
    "account_id": "integer",       // [可选]指定发件账户ID,不传则使用默认账户
    "reply_to_email_id": "integer",// [可选]回复的原始邮件ID
    "reply_type": "string"         // [可选]回复类型:pre_reply/auto_reply/manual_reply
}
```
- **响应**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": "integer",
        "status": "draft",
        "account_id": "integer",
        "recipients": "string",
        "subject": "string",
        // ... 其他邮件信息
    }
}
```

## 发送指定邮件

发送一个已创建的待发送邮件。

- **接口**: `POST /api/user/email-outbox/{email_id}/send`
- **权限**: 需要用户登录
- **路径参数**:
  - `email_id`: 待发送邮件ID
- **响应**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": "integer",
        "status": "sent",          // 发送成功
        "send_time": "datetime",   // 发送时间
        // ... 其他邮件信息
    }
}
```

## 创建并立即发送

创建邮件并立即发送的组合接口。

- **接口**: `POST /api/user/email-outbox/send-direct`
- **权限**: 需要用户登录
- **请求参数**: 同创建待发送邮件
- **响应**: 同发送指定邮件

## 获取发送邮件列表

获取用户的所有发送邮件列表。

- **接口**: `GET /api/user/email-outbox/list`
- **权限**: 需要用户登录
- **查询参数**:
  - `skip`: [可选]跳过记录数,默认0
  - `limit`: [可选]返回记录数,默认100
- **响应**:
```json
{
    "code": 200,
    "message": "success",
    "data": [
        {
            "id": "integer",
            "status": "string",    // draft/pending/sent/failed
            "account_id": "integer",
            "recipients": "string",
            "subject": "string",
            "send_time": "datetime",
            "error_message": "string",
            // ... 其他邮件信息
        }
    ]
}
```

## 获取发送邮件详情

获取单个发送邮件的详细信息。

- **接口**: `GET /api/user/email-outbox/{email_id}`
- **权限**: 需要用户登录
- **路径参数**:
  - `email_id`: 邮件ID
- **响应**:
```json
{
    "code": 200,
    "message": "success",
    "data": {
        "id": "integer",
        "status": "string",
        "account_id": "integer",
        "recipients": "string",
        "cc": "string",
        "bcc": "string",
        "subject": "string",
        "content": "string",
        "content_type": "string",
        "attachments": "string",
        "reply_to_email_id": "integer",
        "reply_type": "string",
        "send_time": "datetime",
        "error_message": "string",
        "created_at": "datetime",
        "updated_at": "datetime"
    }
}
```

## 状态说明

邮件状态(status)包含以下几种:
- `draft`: 草稿状态,刚创建未发送
- `pending`: 待发送状态,已提交发送但尚未完成
- `sent`: 已发送状态,发送成功
- `failed`: 发送失败状态,包含错误信息

## 错误码说明

- `400`: 请求参数错误
  - 找不到可用的邮箱账户
  - 邮件已发送
  - 发送失败(包含具体错误信息)
- `403`: 权限不足
  - 尝试访问其他用户的邮件
- `404`: 资源不存在
  - 邮件不存在 